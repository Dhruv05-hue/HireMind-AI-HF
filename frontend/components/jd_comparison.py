from typing import Any, Dict, Optional
from html import escape

import streamlit as st


def display_jd_comparison(
    jd_comparison: Optional[Dict[str, Any]]
) -> None:

    if not jd_comparison:
        return

    match_pct = float(
        jd_comparison.get("match_percentage", 0) or 0
    )

    semantic = float(
        jd_comparison.get("semantic_similarity", 0) or 0
    )

    match_pct = max(0.0, min(100.0, match_pct))
    semantic_pct = max(
        0.0,
        min(100.0, semantic * 100)
    )

    matched = (
        jd_comparison.get("matched_keywords", [])
        or []
    )

    missing = (
        jd_comparison.get("missing_keywords", [])
        or []
    )

    gap = (
        jd_comparison.get("skills_gap", [])
        or []
    )


    # ========================================================
    # STYLES
    # ========================================================

    st.html(
        """
        <style>

        .jd-wrapper {
            margin-top: 0.5rem;
        }


        .jd-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;

            color: #f8fafc;

            font-size: 1.25rem;
            font-weight: 800;

            margin-bottom: 0.35rem;
        }


        .jd-subtitle {
            color: #64748b;

            font-size: 0.78rem;

            line-height: 1.55;

            margin-bottom: 1.35rem;
        }


        /* ====================================================
           SCORE CARDS
           ==================================================== */

        .jd-score-grid {
            display: grid;

            grid-template-columns:
                repeat(2, minmax(0, 1fr));

            gap: 1rem;

            margin-bottom: 1.4rem;
        }


        .jd-score-card {
            position: relative;

            padding: 1.35rem;

            border-radius: 17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17, 24, 39, 0.97),
                    rgba(10, 15, 28, 0.97)
                );

            border:
                1px solid
                rgba(148, 163, 184, 0.10);

            box-shadow:
                0 10px 30px
                rgba(0, 0, 0, 0.17);

            overflow: hidden;
        }


        .jd-score-card::before {
            content: "";

            position: absolute;

            top: 0;
            left: 0;

            width: 100%;
            height: 2px;

            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #8b5cf6
                );
        }


        .jd-score-label {
            color: #94a3b8;

            font-size: 0.68rem;
            font-weight: 750;

            letter-spacing: 0.06em;
            text-transform: uppercase;

            margin-bottom: 0.45rem;
        }


        .jd-score-value {
            color: #ffffff;

            font-size: 2.25rem;
            line-height: 1;

            font-weight: 850;

            letter-spacing: -0.05em;
        }


        .jd-score-value.gradient {
            background:
                linear-gradient(
                    90deg,
                    #818cf8,
                    #c084fc
                );

            -webkit-background-clip: text;
            background-clip: text;

            -webkit-text-fill-color: transparent;
        }


        .jd-score-description {
            color: #64748b;

            font-size: 0.7rem;

            margin-top: 0.5rem;
        }


        .jd-progress {
            width: 100%;
            height: 7px;

            margin-top: 1rem;

            border-radius: 999px;

            background:
                rgba(255,255,255,0.065);

            overflow: hidden;
        }


        .jd-progress-fill {
            height: 100%;

            border-radius: inherit;

            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #8b5cf6,
                    #a855f7
                );

            box-shadow:
                0 0 14px
                rgba(139,92,246,0.35);
        }


        /* ====================================================
           KEYWORD CARDS
           ==================================================== */

        .jd-content-card {
            padding: 1.25rem;

            border-radius: 17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17,24,39,0.96),
                    rgba(10,15,28,0.96)
                );

            border:
                1px solid
                rgba(148,163,184,0.09);

            margin-bottom: 1rem;
        }


        .jd-content-title {
            display: flex;

            align-items: center;

            gap: 0.5rem;

            color: #e2e8f0;

            font-size: 0.88rem;
            font-weight: 800;

            margin-bottom: 0.9rem;
        }


        .keyword-container {
            display: flex;

            flex-wrap: wrap;

            gap: 0.45rem;
        }


        .keyword-chip {
            display: inline-flex;

            align-items: center;

            padding:
                0.38rem 0.65rem;

            border-radius:
                999px;

            background:
                rgba(99,102,241,0.10);

            border:
                1px solid
                rgba(129,140,248,0.17);

            color:
                #c7d2fe;

            font-size:
                0.7rem;

            font-weight:
                650;
        }


        .missing-chip {
            background:
                rgba(244,63,94,0.08);

            border-color:
                rgba(251,113,133,0.17);

            color:
                #fda4af;
        }


        .gap-chip {
            background:
                rgba(245,158,11,0.08);

            border-color:
                rgba(251,191,36,0.17);

            color:
                #fcd34d;
        }


        .empty-message {
            color:
                #64748b;

            font-size:
                0.75rem;

            line-height:
                1.5;
        }


        /* ====================================================
           BOTTOM GRID
           ==================================================== */

        .jd-bottom-grid {
            display: grid;

            grid-template-columns:
                1fr 1fr;

            gap: 1rem;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 700px) {

            .jd-score-grid {
                grid-template-columns:
                    1fr;
            }

            .jd-bottom-grid {
                grid-template-columns:
                    1fr;
            }

        }

        </style>
        """
    )


    # ========================================================
    # HEADER
    # ========================================================

    st.html(
        """
        <div class="jd-wrapper">

            <div class="jd-title">
                🎯 Job Description Match
            </div>

            <div class="jd-subtitle">
                Compare your resume with the target role's
                keywords, semantic meaning, and required skills.
            </div>

        </div>
        """
    )


    # ========================================================
    # SCORE CARDS
    # ========================================================

    st.html(
        f"""
        <div class="jd-score-grid">

            <div class="jd-score-card">

                <div class="jd-score-label">
                    Match Percentage
                </div>

                <div class="jd-score-value gradient">
                    {match_pct:.0f}%
                </div>

                <div class="jd-score-description">
                    Keyword and requirement alignment
                </div>

                <div class="jd-progress">

                    <div
                        class="jd-progress-fill"
                        style="width: {match_pct:.1f}%;">
                    </div>

                </div>

            </div>


            <div class="jd-score-card">

                <div class="jd-score-label">
                    Semantic Similarity
                </div>

                <div class="jd-score-value">
                    {semantic_pct:.0f}%
                </div>

                <div class="jd-score-description">
                    Meaning-level similarity between resume and JD
                </div>

                <div class="jd-progress">

                    <div
                        class="jd-progress-fill"
                        style="width: {semantic_pct:.1f}%;">
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # MATCHED KEYWORDS
    # ========================================================

    matched_html = ""

    for keyword in matched[:15]:

        safe_keyword = escape(
            str(keyword)
        )

        matched_html += (
            f"""
            <span class="keyword-chip">
                ✓ {safe_keyword}
            </span>
            """
        )


    if not matched_html:

        matched_html = """
        <div class="empty-message">
            No matched keywords detected yet.
        </div>
        """


    st.html(
        f"""
        <div class="jd-content-card">

            <div class="jd-content-title">
                <span>✅</span>
                <span>Matched Keywords</span>
            </div>

            <div class="keyword-container">
                {matched_html}
            </div>

        </div>
        """
    )


    # ========================================================
    # MISSING + SKILLS GAP
    # ========================================================

    missing_html = ""

    for keyword in missing[:10]:

        safe_keyword = escape(
            str(keyword)
        )

        missing_html += (
            f"""
            <span class="keyword-chip missing-chip">
                × {safe_keyword}
            </span>
            """
        )


    if not missing_html:

        missing_html = """
        <div class="empty-message">
            All key terms are present in the current comparison.
        </div>
        """


    gap_html = ""

    for skill in gap[:10]:

        safe_skill = escape(
            str(skill)
        )

        gap_html += (
            f"""
            <span class="keyword-chip gap-chip">
                ⚠ {safe_skill}
            </span>
            """
        )


    if not gap_html:

        gap_html = """
        <div class="empty-message">
            No significant skills gap detected.
        </div>
        """


    st.html(
        f"""
        <div class="jd-bottom-grid">

            <div class="jd-content-card">

                <div class="jd-content-title">
                    <span>❌</span>
                    <span>Missing Keywords</span>
                </div>

                <div class="keyword-container">
                    {missing_html}
                </div>

            </div>


            <div class="jd-content-card">

                <div class="jd-content-title">
                    <span>📊</span>
                    <span>Skills Gap</span>
                </div>

                <div class="keyword-container">
                    {gap_html}
                </div>

            </div>

        </div>
        """
    )