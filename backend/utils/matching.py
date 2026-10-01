from typing import Dict, List

from rapidfuzz import fuzz


SKILL_ALIASES: Dict[str, str] = {
    # JavaScript / frontend
    'reactjs': 'react',
    'react.js': 'react',
    'angularjs': 'angular',
    'vuejs': 'vue',
    'vue.js': 'vue',
    'nextjs': 'next.js',

    # Backend
    'nodejs': 'node.js',
    'node': 'node.js',
    'expressjs': 'express',
    'express.js': 'express',
    'springboot': 'spring boot',

    # Languages / general
    'golang': 'go',

    # AI / ML
    'ml': 'machine learning',
    'ai': 'artificial intelligence',
    'nlp': 'natural language processing',
    'cv': 'computer vision',

    # Tools / platforms
    'k8s': 'kubernetes',
    'sklearn': 'scikit-learn',
    'postgres': 'postgresql',
    'dotnet': '.net',
    'tailwindcss': 'tailwind',
    'amazon web services': 'aws',
    'google cloud': 'gcp',
    'pyspark': 'spark',
    'huggingface': 'hugging face',
}


# Generic phrases that should never be treated as technical skills.
GENERIC_KEYWORDS = {
    'experience',
    'the candidate',
    'candidate',
    'job',
    'role',
    'position',
    'company',
    'team',
    'work',
    'working',
    'responsibility',
    'responsibilities',
    'development',
    'knowledge',
    'ability',
    'skills',
    'skill',
    'requirements',
    'requirement',
    'qualification',
    'qualifications',
    'professional experience',
    'relevant experience',
    'years of experience',
    'strong communication',
    'communication skills',
    'problem solving',
    'problem-solving',
    'an ai/ml engineer',
    'ai/ml engineer',
    'software engineer',
    'engineer',
}


def _clean_text(value: str) -> str:
    """Basic normalization used before canonical skill mapping."""
    return ' '.join(
        value.strip().lower().replace('–', '-').replace('—', '-').split()
    )


def _remove_plural(value: str) -> str:
    """
    Handle common technical plural forms.

    Examples:
        cnns -> cnn
        apis -> api
        models -> model
    """
    if len(value) <= 3:
        return value

    if value.endswith('ies') and len(value) > 4:
        return value[:-3] + 'y'

    if value.endswith('s') and not value.endswith('ss'):
        return value[:-1]

    return value


def normalize_skill(skill: str) -> str:
    """
    Convert skill names into a canonical representation.
    """
    cleaned = _clean_text(str(skill))

    # Direct alias
    if cleaned in SKILL_ALIASES:
        return SKILL_ALIASES[cleaned]

    # Handle common plural forms before alias lookup
    singular = _remove_plural(cleaned)

    if singular in SKILL_ALIASES:
        return SKILL_ALIASES[singular]

    # Normalize common technical variants
    replacements = {
        'rest apis': 'rest api',
        'restful apis': 'rest api',
        'restful api': 'rest api',
        'cnns': 'cnn',
        'rnn networks': 'rnn',
        'rnns': 'rnn',
        'lstms': 'lstm',
        'apis': 'api',
        'machine learning models': 'machine learning',
        'deep learning models': 'deep learning',
        'computer vision applications': 'computer vision',
        'nlp pipelines': 'natural language processing',
    }

    if cleaned in replacements:
        cleaned = replacements[cleaned]

    return cleaned


def is_generic_keyword(keyword: str) -> bool:
    """
    Return True when a keyword is too generic to be useful
    for technical ATS matching.
    """
    cleaned = _clean_text(keyword)

    if not cleaned:
        return True

    if cleaned in GENERIC_KEYWORDS:
        return True

    # Very short generic words are usually not useful ATS skills.
    if len(cleaned) <= 2 and cleaned not in {
        'c', 'r', 'go', 'ai', 'ml', 'nlp', 'cv'
    }:
        return True

    return False


def _split_combined_keywords(keywords: List[str]) -> List[str]:
    """
    Split accidentally combined comma/semicolon/pipe-separated skills.

    Example:
        'Python, PyTorch, TensorFlow'
    becomes:
        ['Python', 'PyTorch', 'TensorFlow']
    """
    result = []

    for keyword in keywords:
        if not isinstance(keyword, str):
            continue

        parts = (
            keyword
            .replace(';', ',')
            .replace('|', ',')
            .split(',')
        )

        for part in parts:
            cleaned = part.strip()

            if cleaned and not is_generic_keyword(cleaned):
                result.append(cleaned)

    return result


def _prepare_keywords(keywords: List[str]) -> List[str]:
    """
    Clean, split, normalize and deduplicate keyword lists.
    """
    prepared = []
    seen = set()

    for keyword in _split_combined_keywords(keywords):
        canonical = normalize_skill(keyword)

        if is_generic_keyword(canonical):
            continue

        if canonical not in seen:
            seen.add(canonical)
            prepared.append(keyword.strip())

    return prepared


def _skills_are_contained(skill_a: str, skill_b: str) -> bool:
    """
    Check whether one normalized skill appears inside the other.

    This handles cases such as:

        computer vision
        computer vision applications

        NLP
        NLP pipelines

        AI systems
        production-oriented AI systems
    """
    a = normalize_skill(skill_a)
    b = normalize_skill(skill_b)

    if not a or not b:
        return False

    if a == b:
        return True

    return a in b or b in a


def _match_score(skill_a: str, skill_b: str) -> int:
    """
    Calculate a robust similarity score between two skills.
    """
    a = normalize_skill(skill_a)
    b = normalize_skill(skill_b)

    if a == b:
        return 100

    # Stronger than fuzzy matching for phrases containing one another.
    if _skills_are_contained(a, b):
        return 95

    token_score = fuzz.token_sort_ratio(a, b)
    partial_score = fuzz.partial_ratio(a, b)

    return max(token_score, partial_score)


def fuzzy_match_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
    threshold: int = 80,
) -> Dict[str, List[str]]:
    """
    Match JD keywords against resume keywords.

    Matching order:
        1. Canonical exact match
        2. Containment match
        3. Fuzzy similarity

    Generic phrases are ignored.
    """

    resume_keywords = _prepare_keywords(resume_keywords)
    jd_keywords = _prepare_keywords(jd_keywords)

    # canonical -> original
    resume_normalized = {
        normalize_skill(keyword): keyword
        for keyword in resume_keywords
    }

    jd_normalized = {
        normalize_skill(keyword): keyword
        for keyword in jd_keywords
    }

    matched_jd_originals = []
    missing_jd_originals = []

    for jd_canon, jd_original in jd_normalized.items():

        # --------------------------------------------------
        # 1. Exact canonical match
        # --------------------------------------------------
        if jd_canon in resume_normalized:
            matched_jd_originals.append(jd_original)
            continue

        # --------------------------------------------------
        # 2. Containment match
        # --------------------------------------------------
        containment_match = False

        for resume_canon in resume_normalized:

            if (
                jd_canon in resume_canon
                or resume_canon in jd_canon
            ):
                containment_match = True
                break

        if containment_match:
            matched_jd_originals.append(jd_original)
            continue

        # --------------------------------------------------
        # 3. Fuzzy match
        # --------------------------------------------------
        best_score = 0

        for resume_canon in resume_normalized:
            score = _match_score(jd_canon, resume_canon)
            best_score = max(best_score, score)

        if best_score >= threshold:
            matched_jd_originals.append(jd_original)
        else:
            missing_jd_originals.append(jd_original)

    return {
        'matched': sorted(set(matched_jd_originals)),
        'missing': sorted(set(missing_jd_originals)),
    }