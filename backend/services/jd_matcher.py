from typing import List, Dict

import numpy as np
import spacy
from rapidfuzz import fuzz

from backend.utils.matching import (
    fuzzy_match_keywords,
    normalize_skill,
    is_generic_keyword,
)
from backend.hf_ml_client import calculate_semantic_similarity


def identify_matched_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
) -> List[str]:
    result = fuzzy_match_keywords(
        resume_keywords,
        jd_keywords,
        threshold=80,
    )

    return result["matched"]


def identify_missing_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
    top_n: int = 15,
) -> List[str]:
    result = fuzzy_match_keywords(
        resume_keywords,
        jd_keywords,
        threshold=80,
    )

    return result["missing"][:top_n]


def _extract_spacy_technical_terms(
    jd_text: str,
    nlp: spacy.Language,
) -> List[str]:
    """
    Extract potentially technical terms from a JD.

    This function deliberately avoids treating every noun phrase
    as a skill. Generic phrases such as "the candidate", "experience",
    and "the team" are ignored.
    """

    doc = nlp(jd_text[:5000])

    candidates = set()

    # ---------------------------------------------------------
    # 1. Named entities that are commonly useful for technical
    #    matching.
    # ---------------------------------------------------------

    for ent in doc.ents:
        if ent.label_ in {
            "PRODUCT",
            "ORG",
            "LANGUAGE",
            "PERSON",
        }:
            value = ent.text.strip()

            if value and not is_generic_keyword(value):
                candidates.add(value)

    # ---------------------------------------------------------
    # 2. Noun chunks are only considered when they contain
    #    technical indicators.
    #
    #    We do NOT add every noun chunk anymore.
    # ---------------------------------------------------------

    technical_indicators = {
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
        "go",
        "golang",
        "rust",
        "php",
        "ruby",
        "swift",
        "kotlin",

        "react",
        "angular",
        "vue",
        "node",
        "node.js",
        "express",
        "spring",
        "spring boot",
        "fastapi",
        "flask",
        "django",

        "sql",
        "mysql",
        "postgres",
        "postgresql",
        "mongodb",
        "redis",
        "oracle",

        "aws",
        "azure",
        "gcp",
        "google cloud",
        "docker",
        "kubernetes",

        "git",
        "github",

        "machine learning",
        "deep learning",
        "artificial intelligence",
        "ai",
        "ml",
        "nlp",
        "natural language processing",
        "computer vision",
        "cnn",
        "cnns",
        "rnn",
        "rnns",
        "lstm",
        "transformer",
        "transformers",
        "pytorch",
        "tensorflow",
        "keras",
        "scikit-learn",
        "sklearn",
        "opencv",
        "mediapipe",

        "rest api",
        "rest apis",
        "graphql",
        "api",

        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "spark",
        "pyspark",
        "hadoop",

        "llm",
        "llms",
        "generative ai",
        "genai",
        "rag",
        "embeddings",
        "vector database",
        "vector databases",
    }

    for chunk in doc.noun_chunks:
        value = chunk.text.strip()

        if not value:
            continue

        normalized = normalize_skill(value)

        if is_generic_keyword(normalized):
            continue

        # Only keep noun chunks containing an actual technical
        # indicator.
        contains_technical_term = any(
            indicator in normalized
            for indicator in technical_indicators
        )

        if contains_technical_term:
            candidates.add(value)

    return sorted(candidates)


def _clean_skill_candidates(
    candidates: List[str],
) -> List[str]:
    """
    Normalize and filter extracted JD skill candidates.
    """

    cleaned = []
    seen = set()

    for candidate in candidates:
        if not isinstance(candidate, str):
            continue

        candidate = candidate.strip()

        if not candidate:
            continue

        # Remove common punctuation surrounding a skill.
        candidate = candidate.strip(".,;:()[]{}")

        if not candidate:
            continue

        if is_generic_keyword(candidate):
            continue

        canonical = normalize_skill(candidate)

        if not canonical:
            continue

        if is_generic_keyword(canonical):
            continue

        if canonical not in seen:
            seen.add(canonical)
            cleaned.append(candidate)

    return cleaned


def _skill_matches_resume(
    jd_skill: str,
    resume_normalized: set,
) -> bool:
    """
    Determine whether a JD skill is already represented
    in the resume skills.

    Matching order:
        1. Exact canonical match
        2. Containment
        3. Fuzzy similarity
    """

    jd_normalized = normalize_skill(jd_skill)

    if not jd_normalized:
        return False

    # ---------------------------------------------------------
    # Exact match
    # ---------------------------------------------------------

    if jd_normalized in resume_normalized:
        return True

    # ---------------------------------------------------------
    # Containment match
    #
    # Examples:
    #   NLP -> NLP pipelines
    #   CNN -> CNNs
    #   Computer Vision -> Computer Vision applications
    # ---------------------------------------------------------

    for resume_skill in resume_normalized:
        if (
            jd_normalized in resume_skill
            or resume_skill in jd_normalized
        ):
            return True

    # ---------------------------------------------------------
    # Fuzzy match
    # ---------------------------------------------------------

    best_score = 0

    for resume_skill in resume_normalized:
        token_score = fuzz.token_sort_ratio(
            jd_normalized,
            resume_skill,
        )

        partial_score = fuzz.partial_ratio(
            jd_normalized,
            resume_skill,
        )

        score = max(
            token_score,
            partial_score,
        )

        best_score = max(
            best_score,
            score,
        )

    return best_score >= 80


def analyze_skills_gap(
    resume_skills: List[str],
    resume_keywords: List[str],
    jd_text: str,
    nlp: spacy.Language,
    jd_keywords: List[str] | None = None,
) -> List[str]:
    """
    Identify technical skills required by the JD but not
    represented anywhere in the resume's skills/keywords.

    Resume evidence comes from:
        1. Explicit resume skills
        2. ATS keywords extracted from the resume

    This keeps skills_gap consistent with matched_keywords
    and missing_keywords.
    """

    # ---------------------------------------------------------
    # Build combined resume evidence
    # ---------------------------------------------------------

    resume_evidence = []

    resume_evidence.extend(
        resume_skills or []
    )

    resume_evidence.extend(
        resume_keywords or []
    )

    # ---------------------------------------------------------
    # Normalize resume evidence
    # ---------------------------------------------------------

    resume_normalized = set()

    for skill in resume_evidence:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        if is_generic_keyword(skill):
            continue

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        if is_generic_keyword(normalized):
            continue

        resume_normalized.add(
            normalized
        )

    # ---------------------------------------------------------
    # No JD keywords
    # ---------------------------------------------------------

    if not jd_keywords:
        return []

    # ---------------------------------------------------------
    # Normalize JD candidates
    # ---------------------------------------------------------

    jd_candidates = []

    seen = set()

    for skill in jd_keywords:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        if is_generic_keyword(skill):
            continue

        normalized = normalize_skill(skill)

        if not normalized:
            continue

        if is_generic_keyword(normalized):
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        jd_candidates.append(
            skill
        )

    # ---------------------------------------------------------
    # Find actual skills gaps
    # ---------------------------------------------------------

    gap = []

    for jd_skill in jd_candidates:

        if _skill_matches_resume(
            jd_skill,
            resume_normalized,
        ):
            continue

        gap.append(
            jd_skill
        )

    return sorted(
        set(gap),
        key=lambda x: x.lower(),
    )[:20]


def calculate_match_percentage(
    resume_keywords: List[str],
    jd_keywords: List[str],
    semantic_similarity: float,
) -> float:
    if not jd_keywords:
        return 0.0

    matched = identify_matched_keywords(
        resume_keywords,
        jd_keywords,
    )

    keyword_overlap = len(matched) / len(jd_keywords)

    # IMPORTANT:
    # Keep the original 60% keyword + 40% semantic weighting.
    match_pct = (
        keyword_overlap * 0.6
        + semantic_similarity * 0.4
    ) * 100

    return float(
        np.clip(match_pct, 0.0, 100.0)
    )


def compare_resume_with_jd(
    resume_text: str,
    resume_keywords: List[str],
    resume_skills: List[str],
    jd_text: str,
    jd_keywords: List[str],
    nlp: spacy.Language,
) -> Dict:
    """
    Compare a resume against a job description using:

    1. Keyword matching
    2. Semantic similarity through the Hugging Face ML service
    3. Technical skill-gap analysis
    """

    semantic_similarity = calculate_semantic_similarity(
        resume_text,
        jd_text,
    )

    matched_keywords = identify_matched_keywords(
        resume_keywords,
        jd_keywords,
    )

    missing_keywords = identify_missing_keywords(
        resume_keywords,
        jd_keywords,
    )

    skills_gap = analyze_skills_gap(
        resume_skills=resume_skills,
        resume_keywords=resume_keywords,
        jd_text=jd_text,
        nlp=nlp,
        jd_keywords=jd_keywords,
    )

    match_percentage = calculate_match_percentage(
        resume_keywords,
        jd_keywords,
        semantic_similarity,
    )

    return {
        "match_percentage": match_percentage,
        "semantic_similarity": semantic_similarity,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "skills_gap": skills_gap,
    }