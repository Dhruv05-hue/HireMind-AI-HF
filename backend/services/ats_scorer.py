import re
import spacy
import numpy as np
from backend.hf_ml_client import (
    calculate_semantic_similarity,
    calculate_batch_semantic_similarity,
)
from typing import Dict, List, Optional, Tuple

from backend.utils.file_utils import log_warning
from backend.utils.matching import (
    fuzzy_match_keywords,
    normalize_skill,
    is_generic_keyword,
)


ZIP_CODE_PATTERN = r'\b\d{5}(?:-\d{4})?\b'

STREET_ADDRESS_PATTERN = (
    r'\b\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+'
    r'(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|'
    r'Drive|Dr|Court|Ct|Circle|Cir|Way|Place|Pl)\b'
)


def _tier_score(n: float, tiers: list) -> float:
    for threshold, pts in tiers:
        if n >= threshold:
            return pts

    return 0.0


# ============================================================
# LOCATION / PRIVACY DETECTION
# ============================================================

def detect_location_info(
    text: str,
    nlp: spacy.Language,
) -> Dict:

    locations = []

    # Method 01: spaCy NER
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:
            locations.append({
                'text': ent.text,
                'type': ent.label_.lower(),
                'start': ent.start_char,
            })

    # Method 02: street address regex
    for match in re.finditer(
        STREET_ADDRESS_PATTERN,
        text,
        re.IGNORECASE,
    ):
        locations.append({
            'text': match.group(),
            'type': 'address',
            'start': match.start(),
        })

    # Method 03: ZIP/PIN code regex
    for match in re.finditer(
        ZIP_CODE_PATTERN,
        text,
    ):
        locations.append({
            'text': match.group(),
            'type': 'zip',
            'start': match.start(),
        })

    has_address = any(
        loc['type'] == 'address'
        for loc in locations
    )

    has_zip = any(
        loc['type'] == 'zip'
        for loc in locations
    )

    if has_address and has_zip:
        privacy_risk, penalty = 'high', 5.0

    elif has_address or has_zip:
        privacy_risk, penalty = 'high', 4.0

    elif len(locations) > 3:
        privacy_risk, penalty = 'medium', 3.0

    elif locations:
        privacy_risk, penalty = 'low', 2.0

    else:
        privacy_risk, penalty = 'none', 0.0

    recommendations = []

    if not locations:
        recommendations.append(
            "No privacy concerns detected."
        )

    if has_address:
        recommendations.append(
            "Remove full street addresses — ATS systems don't need this and it's a privacy risk."
        )

    if has_zip:
        recommendations.append(
            "Remove zip codes — this level of location detail is unnecessary."
        )

    if (
        privacy_risk in ('low', 'medium')
        and not has_address
        and not has_zip
    ):
        recommendations.append(
            "Consider reducing location mentions. 'City, State' in the contact header is sufficient."
        )

    return {
        'location_found': len(locations) > 0,
        'detected_locations': locations,
        'privacy_risk': privacy_risk,
        'recommendations': recommendations,
        'penalty_applied': penalty,
    }


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

def _calculate_semantic_similarity(
    skill: str,
    text: str,
) -> float:
    """
    Calculate semantic similarity between a skill and a body of text
    using the Hugging Face ML service.
    """

    if not skill or not text:
        return 0.0

    try:
        similarity = calculate_semantic_similarity(
            skill,
            text,
        )

        return float(
            max(
                0.0,
                min(1.0, similarity),
            )
        )

    except Exception as e:
        log_warning(
            f"Similarity error for '{skill}': {e}",
            context='ats_scorer',
        )

        return 0.0


# ============================================================
# SKILL MATCHING
# ============================================================

def _normalize_text(text: str) -> str:
    """
    Normalize text for reliable skill matching.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    # Normalize common punctuation.
    text = text.replace(
        '–',
        '-',
    ).replace(
        '—',
        '-',
    )

    # Collapse whitespace.
    text = re.sub(
        r'\s+',
        ' ',
        text,
    )

    return text.strip()


def _skill_text_variants(skill: str) -> List[str]:
    """
    Generate useful normalized variants for a skill.

    Example:
        REST APIs -> ['rest api', 'rest apis']
        CNNs     -> ['cnn', 'cnns']
    """

    if not isinstance(skill, str):
        return []

    cleaned = _normalize_text(skill)

    if not cleaned:
        return []

    canonical = normalize_skill(cleaned)

    variants = {
        cleaned,
        canonical,
    }

    # Common plural variants.
    if canonical.endswith('s') and not canonical.endswith('ss'):
        variants.add(canonical[:-1])
    else:
        variants.add(canonical + 's')

    # Explicit technical variants.
    replacements = {
        'rest api': [
            'rest api',
            'rest apis',
            'restful api',
            'restful apis',
        ],
        'cnn': [
            'cnn',
            'cnns',
            'convolutional neural network',
            'convolutional neural networks',
        ],
        'rnn': [
            'rnn',
            'rnns',
            'recurrent neural network',
            'recurrent neural networks',
        ],
        'lstm': [
            'lstm',
            'lstms',
            'long short-term memory',
        ],
        'nlp': [
            'nlp',
            'natural language processing',
            'nlp pipelines',
        ],
        'computer vision': [
            'computer vision',
            'computer vision applications',
        ],
        'machine learning': [
            'machine learning',
            'machine learning models',
            'ml',
        ],
        'deep learning': [
            'deep learning',
            'deep learning models',
        ],
        'artificial intelligence': [
            'artificial intelligence',
            'ai',
        ],
        'scikit-learn': [
            'scikit-learn',
            'sklearn',
        ],
        'node.js': [
            'node.js',
            'nodejs',
            'node',
        ],
        'postgresql': [
            'postgresql',
            'postgres',
        ],
    }

    if canonical in replacements:
        variants.update(
            replacements[canonical]
        )

    return list(variants)


def _skill_matches_text(
    skill: str,
    text: str,
) -> Tuple[bool, float]:
    """
    Fast deterministic skill matching.

    This is intentionally performed before semantic similarity.

    Matching levels:

        1. Exact phrase
        2. Normalized variant
        3. Word-boundary match
    """

    if not skill or not text:
        return False, 0.0

    normalized_text = _normalize_text(text)

    if not normalized_text:
        return False, 0.0

    variants = _skill_text_variants(skill)

    # --------------------------------------------------------
    # Exact / phrase matching
    # --------------------------------------------------------

    for variant in variants:
        variant = _normalize_text(variant)

        if not variant:
            continue

        # Word-boundary matching prevents cases such as:
        #
        # "go" matching "google"
        #
        pattern = r'(?<!\w)' + re.escape(variant) + r'(?!\w)'

        if re.search(
            pattern,
            normalized_text,
            re.IGNORECASE,
        ):
            return True, 1.0

    # --------------------------------------------------------
    # Token containment for phrases
    # --------------------------------------------------------

    canonical = normalize_skill(skill)

    if canonical:

        text_without_punctuation = re.sub(
            r'[^a-z0-9+#.\- ]',
            ' ',
            normalized_text,
        )

        text_without_punctuation = re.sub(
            r'\s+',
            ' ',
            text_without_punctuation,
        ).strip()

        if canonical in text_without_punctuation:
            return True, 0.98

    return False, 0.0


def _skill_matches(
    skill: str,
    text: str,
    threshold: float = 0.6,
) -> Tuple[bool, float]:
    """
    Determine whether a skill is supported by a body of text.

    Priority:

        1. Exact technical phrase
        2. Normalized alias / plural variant
        3. Semantic similarity through the Hugging Face ML service

    Semantic similarity is used only as a fallback because
    relying on embeddings alone can create false positives.
    """

    if not skill or not text:
        return False, 0.0

    # --------------------------------------------------------
    # Deterministic matching first
    # --------------------------------------------------------

    matched, score = _skill_matches_text(
        skill,
        text,
    )

    if matched:
        return True, score

    # --------------------------------------------------------
    # Semantic fallback
    # --------------------------------------------------------

    similarity = _calculate_semantic_similarity(
        skill,
        text,
    )

    return (
        similarity >= threshold,
        similarity,
    )


# ============================================================
# SKILL VALIDATION
# ============================================================

def validate_skills_with_projects(
    skills: List[str],
    projects: List[Dict],
    experience_entries: List[Dict],
    threshold: float = 0.60,
) -> Dict:
    """
    Validate resume skills against actual project and
    experience evidence.

    Deterministic matching is performed first.

    Skills that are not deterministically matched are collected
    and sent to the Hugging Face ML service in one batch request.
    This preserves the existing semantic fallback behavior while
    avoiding one network request per skill/evidence pair.

    Each skill is checked against:

        - Project title
        - Project description
        - Project technologies
        - Experience job title
        - Experience company
        - Experience description
    """

    if not skills:
        return {
            'validated_skills': [],
            'unvalidated_skills': [],
            'validation_percentage': 0.0,
            'skill_project_mapping': {},
            'validation_score': 0.0,
        }

    # --------------------------------------------------------
    # Prepare experience text
    # --------------------------------------------------------

    experience_text = ' '.join(
        ' '.join(
            str(e.get(field) or '')
            for field in [
                'job_title',
                'company',
                'description',
            ]
        )
        for e in experience_entries
        if isinstance(e, dict)
    ).strip()

    validated_skills = []
    unvalidated_skills = []
    skill_project_mapping = {}

    # --------------------------------------------------------
    # Prepare semantic fallback candidates
    #
    # Every candidate is represented by:
    #   (skill, evidence_text, result_type, result_index, title)
    #
    # result_type:
    #   "project" or "experience"
    # --------------------------------------------------------

    semantic_candidates = []
    skill_results = []

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        if is_generic_keyword(skill):
            continue

        matching_projects = []
        max_similarity = 0.0

        project_candidates = []

        # ====================================================
        # PROJECT VALIDATION
        # ====================================================

        for project_index, project in enumerate(projects):

            if not isinstance(project, dict):
                continue

            project_title = str(
                project.get('title') or ''
            )

            project_description = str(
                project.get('description') or ''
            )

            # Include technologies extracted by Groq.
            technologies = project.get(
                'technologies',
                [],
            )

            if not isinstance(
                technologies,
                list,
            ):
                technologies = []

            technologies_text = ' '.join(
                str(technology)
                for technology in technologies
                if technology
            )

            project_text = ' '.join(
                [
                    project_title,
                    project_description,
                    technologies_text,
                ]
            ).strip()

            if not project_text:
                continue

            # Deterministic matching first.
            matched, similarity = _skill_matches_text(
                skill,
                project_text,
            )

            if matched:
                max_similarity = max(
                    max_similarity,
                    similarity,
                )

                title = (
                    project_title
                    or 'Untitled Project'
                )

                if title not in matching_projects:
                    matching_projects.append(title)

            else:
                project_candidates.append(
                    (
                        project_index,
                        project_text,
                        project_title or 'Untitled Project',
                    )
                )

        # ====================================================
        # EXPERIENCE VALIDATION
        # ====================================================

        experience_candidate = None

        if experience_text:
            matched, similarity = _skill_matches_text(
                skill,
                experience_text,
            )

            if matched:
                max_similarity = max(
                    max_similarity,
                    similarity,
                )

                matching_projects.append(
                    'Experience Section'
                )
            else:
                experience_candidate = experience_text

        skill_results.append(
            {
                'skill': skill,
                'matching_projects': matching_projects,
                'max_similarity': max_similarity,
                'project_candidates': project_candidates,
                'experience_candidate': experience_candidate,
            }
        )

        # Add only the candidates that actually need semantic fallback.
        for project_index, project_text, project_title in project_candidates:
            semantic_candidates.append(
                {
                    'skill_index': len(skill_results) - 1,
                    'text_a': skill,
                    'text_b': project_text,
                    'result_type': 'project',
                    'result_index': project_index,
                    'title': project_title,
                }
            )

        if experience_candidate:
            semantic_candidates.append(
                {
                    'skill_index': len(skill_results) - 1,
                    'text_a': skill,
                    'text_b': experience_candidate,
                    'result_type': 'experience',
                    'result_index': None,
                    'title': 'Experience Section',
                }
            )

    # --------------------------------------------------------
    # Batch semantic fallback
    # --------------------------------------------------------

    if semantic_candidates:

        pairs = [
            (
                candidate['text_a'],
                candidate['text_b'],
            )
            for candidate in semantic_candidates
        ]

        similarities = calculate_batch_semantic_similarity(
            pairs
        )

        for candidate, similarity in zip(
            semantic_candidates,
            similarities,
        ):
            skill_result = skill_results[
                candidate['skill_index']
            ]

            similarity = float(
                max(
                    0.0,
                    min(1.0, similarity),
                )
            )

            skill_result['max_similarity'] = max(
                skill_result['max_similarity'],
                similarity,
            )

            if similarity >= threshold:

                if candidate['result_type'] == 'project':
                    title = candidate['title']

                    if title not in skill_result[
                        'matching_projects'
                    ]:
                        skill_result[
                            'matching_projects'
                        ].append(title)

                elif candidate['result_type'] == 'experience':

                    if 'Experience Section' not in skill_result[
                        'matching_projects'
                    ]:
                        skill_result[
                            'matching_projects'
                        ].append(
                            'Experience Section'
                        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    for skill_result in skill_results:

        skill = skill_result['skill']
        matching_projects = skill_result[
            'matching_projects'
        ]
        max_similarity = skill_result[
            'max_similarity'
        ]

        if matching_projects:

            validated_skills.append(
                {
                    'skill': skill,
                    'projects': matching_projects,
                    'similarity': round(
                        max_similarity,
                        3,
                    ),
                }
            )

            skill_project_mapping[
                skill
            ] = matching_projects

        else:

            unvalidated_skills.append(
                skill
            )

            skill_project_mapping[
                skill
            ] = []

    # --------------------------------------------------------
    # Calculate validation score
    # --------------------------------------------------------

    total_skills = (
        len(validated_skills)
        + len(unvalidated_skills)
    )

    validation_percentage = (
        len(validated_skills)
        / total_skills
        if total_skills > 0
        else 0.0
    )

    validation_score = (
        validation_percentage * 15.0
    )

    return {
        'validated_skills': validated_skills,
        'unvalidated_skills': unvalidated_skills,
        'validation_percentage': validation_percentage,
        'skill_project_mapping': skill_project_mapping,
        'validation_score': validation_score,
    }


# ============================================================
# 01: FORMATTING SCORE
# ============================================================

def _calc_formatting_score(
    parsed_resume: Dict,
    text: str,
) -> float:

    score = 0.0

    exp_entries = [
        e
        for e in parsed_resume.get(
            'experience',
            [],
        )
        if isinstance(e, dict)
    ]

    edu_entries = [
        e
        for e in parsed_resume.get(
            'education',
            [],
        )
        if isinstance(e, dict)
    ]

    skills = parsed_resume.get(
        'skills',
        [],
    )

    summary = parsed_resume.get(
        'professional_summary',
        '',
    )

    proj_entries = [
        p
        for p in parsed_resume.get(
            'projects',
            [],
        )
        if isinstance(p, dict)
    ]

    if (
        exp_entries
        and any(
            e.get('job_title')
            or e.get('description')
            for e in exp_entries
        )
    ):
        score += 3.0

    if edu_entries:
        score += 2.0

    if len(skills) >= 3:
        score += 2.0

    if len(summary) > 30:
        score += 1.5

    if proj_entries:
        score += 1.5

    bullet_count = sum(
        1
        for line in text.split('\n')
        if re.match(
            r'^\s*[•\-\*\◦]',
            line,
        )
        or re.match(
            r'^\s*\d+\.',
            line,
        )
    )

    score += _tier_score(
        bullet_count,
        [
            (15, 5.0),
            (10, 4.0),
            (5, 3.0),
            (3, 2.0),
            (1, 1.0),
        ],
    )

    filled = sum(
        1
        for has_it in [
            bool(exp_entries),
            bool(edu_entries),
            bool(skills),
            bool(summary.strip()),
            bool(proj_entries),
        ]
        if has_it
    )

    score += _tier_score(
        filled,
        [
            (4, 5.0),
            (3, 4.0),
            (2, 3.0),
            (1, 2.0),
        ],
    )

    return min(
        20.0,
        max(0.0, score),
    )


# ============================================================
# 02: KEYWORD SCORE
# ============================================================

def _calc_keywords_score(
    resume_keywords: List[str],
    skills: List[str],
    jd_keywords: Optional[List[str]] = None,
) -> float:

    score = 0.0

    score += _tier_score(
        len(resume_keywords),
        [
            (20, 10.0),
            (15, 8.0),
            (10, 6.0),
            (5, 4.0),
            (3, 2.0),
        ],
    )

    score += _tier_score(
        len(skills),
        [
            (15, 10.0),
            (10, 8.0),
            (7, 6.0),
            (5, 4.0),
            (3, 2.0),
        ],
    )

    if jd_keywords:

        all_resume_terms = list(
            set(
                (resume_keywords or [])
                + (skills or [])
            )
        )

        fuzzy_result = fuzzy_match_keywords(
            all_resume_terms,
            jd_keywords,
            threshold=80,
        )

        match_pct = (
            len(fuzzy_result['matched'])
            / len(jd_keywords)
            if jd_keywords
            else 0
        )

        score += _tier_score(
            match_pct,
            [
                (0.7, 5.0),
                (0.5, 4.0),
                (0.3, 3.0),
                (0.2, 2.0),
                (0.1, 1.0),
            ],
        )

    elif len(resume_keywords) >= 10:
        score += 3.0

    return min(
        25.0,
        max(0.0, score),
    )


# ============================================================
# 03: CONTENT QUALITY SCORE
# ============================================================

def _calc_content_score(
    text: str,
    action_verbs: List[str],
    grammar_results: Dict,
) -> float:

    score = 0.0

    score += _tier_score(
        len(action_verbs),
        [
            (15, 10.0),
            (10, 8.0),
            (7, 6.0),
            (5, 4.0),
            (3, 2.0),
        ],
    )

    number_patterns = [
        r'\d+%',
        r'\$\d+',
        r'\d+[kKmMbB]',
        r'\d+\s*(?:users|customers|clients|projects|hours|days|months|years)',
        r'(?:increased|decreased|improved|reduced|grew|saved)\s+(?:by\s+)?\d+',
    ]

    achievement_count = sum(
        len(
            re.findall(
                pattern,
                text,
                re.IGNORECASE,
            )
        )
        for pattern in number_patterns
    )

    score += _tier_score(
        achievement_count,
        [
            (10, 5.0),
            (7, 4.0),
            (5, 3.0),
            (3, 2.0),
            (1, 1.0),
        ],
    )

    grammar_penalty = grammar_results.get(
        'penalty_applied',
        0.0,
    )

    score += max(
        0.0,
        10.0 - grammar_penalty / 2.0,
    )

    return min(
        25.0,
        max(0.0, score),
    )


# ============================================================
# 04: SKILL VALIDATION SCORE
# ============================================================

def _calc_skill_validation_score(
    validation_results: Dict,
) -> float:

    return min(
        15.0,
        max(
            0.0,
            validation_results.get(
                'validation_score',
                0.0,
            ),
        ),
    )


# ============================================================
# 05: ATS COMPATIBILITY SCORE
# ============================================================

def _calc_ats_compatibility_score(
    text: str,
    location_results: Dict,
    parsed_resume: Dict,
) -> float:

    score = 15.0

    # Deduction 01: location/privacy
    score -= location_results.get(
        'penalty_applied',
        0.0,
    )

    # Deduction 02: unusual formatting characters
    special_chars = len(
        re.findall(
            r'[│┤├┼┴┬╔╗╚╝═║╠╣╦╩╬]',
            text,
        )
    )

    if special_chars > 20:
        score -= 2.0

    elif special_chars > 10:
        score -= 1.0

    exp_entries = [
        e
        for e in parsed_resume.get(
            'experience',
            [],
        )
        if isinstance(e, dict)
    ]

    edu_entries = [
        e
        for e in parsed_resume.get(
            'education',
            [],
        )
        if isinstance(e, dict)
    ]

    skills_count = len(
        parsed_resume.get(
            'skills',
            [],
        )
    )

    exp_desc_len = sum(
        len(
            e.get(
                'description',
                '',
            )
        )
        for e in exp_entries
    )

    edu_desc_len = sum(
        len(
            (e.get('degree') or '')
            + (e.get('institution') or '')
        )
        for e in edu_entries
    )

    # Deduction 03: short sections
    short_sections = sum([
        bool(exp_entries)
        and exp_desc_len < 20,

        bool(edu_entries)
        and edu_desc_len < 20,

        bool(
            parsed_resume.get('skills')
        )
        and skills_count < 2,
    ])

    if short_sections >= 2:
        score -= 2.0

    elif short_sections >= 1:
        score -= 1.0

    if exp_entries and skills_count > 5:
        score += 1.0

    return min(
        15.0,
        max(0.0, score),
    )


# ============================================================
# SCORE AGGREGATION
# ============================================================

def calculate_overall_score(
    text: str,
    parsed_resume: Dict,
    skills: List[str],
    keywords: List[str],
    action_verbs: List[str],
    skill_validation_results: Dict,
    grammar_results: Dict,
    location_results: Dict,
    jd_keywords: Optional[List[str]] = None,
    experience_months: int = 0,
) -> Dict:

    formatting_score = _calc_formatting_score(
        parsed_resume,
        text,
    )

    keywords_score = _calc_keywords_score(
        keywords,
        skills,
        jd_keywords,
    )

    content_score = _calc_content_score(
        text,
        action_verbs,
        grammar_results,
    )

    skill_validation_score = (
        _calc_skill_validation_score(
            skill_validation_results
        )
    )

    ats_compatibility_score = (
        _calc_ats_compatibility_score(
            text,
            location_results,
            parsed_resume,
        )
    )

    COMPONENT_MAX = {
        'formatting': 20.0,
        'keywords': 25.0,
        'content': 25.0,
        'skill_validation': 15.0,
        'ats_compatibility': 15.0,
    }

    formatting_pct = (
        formatting_score
        / COMPONENT_MAX['formatting']
    ) * 100.0

    keywords_pct = (
        keywords_score
        / COMPONENT_MAX['keywords']
    ) * 100.0

    content_pct = (
        content_score
        / COMPONENT_MAX['content']
    ) * 100.0

    skill_validation_pct = (
        skill_validation_score
        / COMPONENT_MAX['skill_validation']
    ) * 100.0

    ats_compatibility_pct = (
        ats_compatibility_score
        / COMPONENT_MAX['ats_compatibility']
    ) * 100.0

    skills_keywords_pct = (
        keywords_pct * 0.6
    ) + (
        skill_validation_pct * 0.4
    )

    base_score = (
        skills_keywords_pct * 0.40
        + content_pct * 0.30
        + formatting_pct * 0.15
        + ats_compatibility_pct * 0.15
    )

    penalties = {}
    bonuses = {}

    score = base_score

    if grammar_results.get(
        'penalty_applied',
        0.0,
    ) > 0:
        penalties['grammar'] = (
            grammar_results[
                'penalty_applied'
            ]
        )

    if location_results.get(
        'penalty_applied',
        0.0,
    ) > 0:
        penalties['location_privacy'] = (
            location_results[
                'penalty_applied'
            ]
        )

    validation_pct = (
        skill_validation_results.get(
            'validation_percentage',
            0.0,
        )
    )

    if validation_pct >= 0.9:
        bonuses[
            'excellent_skill_validation'
        ] = 2.0

        score += 2.0

    elif validation_pct >= 0.8:
        bonuses[
            'good_skill_validation'
        ] = 1.0

        score += 1.0

    if grammar_results.get(
        'total_errors',
        0,
    ) == 0:

        bonuses[
            'perfect_grammar'
        ] = 1.0

        score += 1.0

    if jd_keywords and len(jd_keywords) > 0:

        all_resume_terms = list(
            set(
                (keywords or [])
                + (skills or [])
            )
        )

        fuzzy_result = fuzzy_match_keywords(
            all_resume_terms,
            jd_keywords,
            threshold=80,
        )

        missing_pct = (
            len(fuzzy_result['missing'])
            / len(jd_keywords)
        )

        if missing_pct > 0.7:
            penalties[
                'missing_jd_keywords'
            ] = 15.0

            score -= 15.0

        elif missing_pct > 0.5:
            penalties[
                'missing_jd_keywords'
            ] = 10.0

            score -= 10.0

        elif missing_pct > 0.3:
            penalties[
                'missing_jd_keywords'
            ] = 5.0

            score -= 5.0

    overall_score = min(
        100.0,
        max(0.0, score),
    )

    interpretation = (
        _generate_score_interpretation(
            overall_score
        )
    )

    return {
        'overall_score': round(
            overall_score,
            1,
        ),
        'formatting_score': round(
            formatting_score,
            1,
        ),
        'keywords_score': round(
            keywords_score,
            1,
        ),
        'content_score': round(
            content_score,
            1,
        ),
        'skill_validation_score': round(
            skill_validation_score,
            1,
        ),
        'ats_compatibility_score': round(
            ats_compatibility_score,
            1,
        ),
        'overall_interpretation': interpretation,
        'penalties': penalties,
        'bonuses': bonuses,
    }


# ============================================================
# STRENGTHS
# ============================================================

def generate_strengths(
    score_results: Dict,
    skill_validation_results: Dict,
    grammar_results: Dict,
) -> List[str]:

    strengths = []

    if score_results[
        'formatting_score'
    ] >= 16:

        strengths.append(
            'Well-structured with clear sections and bullet points'
        )

    if score_results[
        'keywords_score'
    ] >= 20:

        strengths.append(
            'Strong keyword optimization and skills presence'
        )

    if score_results[
        'content_score'
    ] >= 20:

        strengths.append(
            'Excellent use of action verbs and quantifiable achievements'
        )

    if score_results[
        'skill_validation_score'
    ] >= 12:

        pct = (
            skill_validation_results.get(
                'validation_percentage',
                0,
            )
            * 100
        )

        strengths.append(
            f'{pct:.0f}% of skills are validated by projects'
        )

    if score_results[
        'ats_compatibility_score'
    ] >= 13:

        strengths.append(
            'Excellent ATS compatibility with clean formatting'
        )

    if grammar_results.get(
        'total_errors',
        0,
    ) == 0:

        strengths.append(
            'Error-free grammar and spelling'
        )

    if not strengths:
        strengths.append(
            'Your resume has potential - focus on the recommendations below'
        )

    return strengths


# ============================================================
# CRITICAL ISSUES
# ============================================================

def generate_critical_issues(
    score_results: Dict,
    grammar_results: Dict,
    location_results: Dict,
) -> List[str]:

    issues = []

    critical_errors = len(
        grammar_results.get(
            'critical_errors',
            [],
        )
    )

    if critical_errors > 0:
        issues.append(
            f'{critical_errors} critical grammar/spelling error(s) detected'
        )

    if location_results.get(
        'privacy_risk'
    ) == 'high':

        issues.append(
            'High privacy risk: Remove detailed location information'
        )

    if score_results[
        'formatting_score'
    ] < 10:

        issues.append(
            'Poor formatting: Add clear sections and bullet points'
        )

    if score_results[
        'keywords_score'
    ] < 12:

        issues.append(
            'Insufficient keywords and technical skills'
        )

    if score_results[
        'skill_validation_score'
    ] < 7:

        issues.append(
            'Most skills lack supporting evidence in projects'
        )

    return issues


# ============================================================
# ACTIONABLE IMPROVEMENTS
# ============================================================

def generate_improvements(
    score_results: Dict,
    skill_validation_results: Dict,
) -> List[str]:

    improvements = []

    if (
        12
        <= score_results['formatting_score']
        < 16
    ):
        improvements.append(
            'Add more bullet points and improve section organization'
        )

    if (
        14
        <= score_results['keywords_score']
        < 20
    ):
        improvements.append(
            'Include more relevant keywords and technical skills'
        )

    if (
        14
        <= score_results['content_score']
        < 20
    ):
        improvements.append(
            'Add more quantifiable achievements and action verbs'
        )

    if (
        7
        <= score_results['skill_validation_score']
        < 12
    ):
        unvalidated_count = len(
            skill_validation_results.get(
                'unvalidated_skills',
                [],
            )
        )

        improvements.append(
            f'Validate {unvalidated_count} skill(s) by adding relevant project details'
        )

    if (
        9
        <= score_results['ats_compatibility_score']
        < 13
    ):
        improvements.append(
            'Simplify formatting for better ATS compatibility'
        )

    return improvements


# ============================================================
# SCORE INTERPRETATION
# ============================================================

def _generate_score_interpretation(
    overall_score: float,
) -> str:

    if overall_score >= 90:
        return (
            'Excellent! Your resume is highly optimized for ATS systems.'
        )

    elif overall_score >= 80:
        return (
            'Great! Your resume should perform well with most ATS systems.'
        )

    elif overall_score >= 70:
        return (
            'Good! Your resume is ATS-friendly with room for minor improvements.'
        )

    elif overall_score >= 60:
        return (
            'Fair. Your resume needs some improvements to be fully ATS-compatible.'
        )

    elif overall_score >= 50:
        return (
            'Below Average. Significant improvements needed for ATS compatibility.'
        )

    else:
        return (
            'Poor. Your resume requires major revisions to pass ATS screening.'
        )