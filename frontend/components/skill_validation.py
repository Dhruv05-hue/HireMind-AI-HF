from typing import Any, Dict
from html import escape

import streamlit as st


def display_skill_validation(analysis: Dict[str, Any]) -> None:
    """
    Display skill validation results with a modern HireMind AI UI.

    Backend data and validation logic are unchanged.
    This component only controls presentation.
    """

    details = analysis.get("skill_validation_details") or {}

    validated = details.get("validated", []) or []
    unvalidated = details.get("unvalidated", []) or []

    total = details.get(
        "total",
        len(validated) + len(unvalidated),
    )

    pct = float(
        details.get("validation_pct", 0.0) or 0.0
    )

    pct = max(0.0, min(100.0, pct))

    # ========================================================
    # GLOBAL STYLES
    # ========================================================

    st.html(
        """
        <style>

        /* ====================================================
           STAT CARDS
           ==================================================== */

        .skill-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-bottom: 1.25rem;
        }


        .skill-stat-card {
            position: relative;

            padding: 1.25rem 1.3rem;
            min-height: 110px;

            border-radius: 16px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17, 24, 39, 0.96),
                    rgba(10, 15, 28, 0.96)
                );

            border:
                1px solid
                rgba(148, 163, 184, 0.10);

            box-shadow:
                0 8px 25px
                rgba(0, 0, 0, 0.16);

            overflow: hidden;
        }


        .skill-stat-card::before {
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


        .skill-stat-label {
            color: #94a3b8;

            font-size: 0.72rem;
            font-weight: 700;

            letter-spacing: 0.04em;
            text-transform: uppercase;

            margin-bottom: 0.45rem;
        }


        .skill-stat-value {
            color: #f8fafc;

            font-size: 2rem;
            line-height: 1;

            font-weight: 850;

            letter-spacing: -0.04em;
        }


        .skill-stat-value.validation {
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


        .skill-stat-subtitle {
            color: #64748b;

            font-size: 0.68rem;

            margin-top: 0.5rem;
        }


        /* ====================================================
           VALIDATION PROGRESS
           ==================================================== */

        .validation-progress-wrapper {
            margin: 0.5rem 0 1.35rem 0;
        }


        .validation-progress-top {
            display: flex;

            justify-content: space-between;
            align-items: center;

            margin-bottom: 0.45rem;
        }


        .validation-progress-label {
            color: #94a3b8;

            font-size: 0.72rem;
            font-weight: 650;
        }


        .validation-progress-value {
            color: #c4b5fd;

            font-size: 0.72rem;
            font-weight: 750;
        }


        .validation-progress {
            width: 100%;
            height: 8px;

            border-radius: 999px;

            background:
                rgba(255, 255, 255, 0.07);

            overflow: hidden;
        }


        .validation-progress-fill {
            height: 100%;

            border-radius: inherit;

            background:
                linear-gradient(
                    90deg,
                    #3b82f6,
                    #6366f1,
                    #8b5cf6
                );

            box-shadow:
                0 0 14px
                rgba(99, 102, 241, 0.40);

            transition:
                width 0.6s ease;
        }


        /* ====================================================
           EXPANDER CONTENT
           ==================================================== */

        .skill-list-item {
            padding: 0.7rem 0;

            border-bottom:
                1px solid
                rgba(148, 163, 184, 0.07);
        }


        .skill-list-item:last-child {
            border-bottom: none;
        }


        .skill-name {
            color: #f1f5f9;

            font-size: 0.83rem;
            font-weight: 700;
        }


        .skill-detail {
            color: #94a3b8;

            font-size: 0.74rem;

            line-height: 1.5;

            margin-top: 0.25rem;
        }


        .skill-match {
            color: #6ee7b7;

            font-weight: 700;
        }


        .skill-description {
            color: #64748b;

            font-size: 0.74rem;

            line-height: 1.5;

            margin:
                0 0 0.75rem 0;
        }


        /* ====================================================
           EMPTY STATE
           ==================================================== */

        .skill-empty-state {
            padding: 1.25rem 1.4rem;

            border-radius: 14px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17, 24, 39, 0.96),
                    rgba(10, 15, 28, 0.96)
                );

            border:
                1px solid
                rgba(148, 163, 184, 0.10);

            color: #94a3b8;

            text-align: center;

            font-size: 0.85rem;
        }


        .skill-empty-title {
            color: #f8fafc;

            font-size: 0.95rem;
            font-weight: 750;

            margin-bottom: 0.35rem;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 700px) {

            .skill-stats {
                grid-template-columns: 1fr;
            }

        }

        </style>
        """
    )


    # ========================================================
    # EMPTY STATE
    # ========================================================

    if total == 0:

        st.html(
            """
            <div class="skill-empty-state">

                <div class="skill-empty-title">
                    ✓ No Skills Detected
                </div>

                <div>
                    No skills were detected on the resume.
                </div>

            </div>
            """
        )

        return


    # ========================================================
    # STATISTICS
    # ========================================================

    st.html(
        f"""
        <div class="skill-stats">

            <div class="skill-stat-card">

                <div class="skill-stat-label">
                    Total Skills
                </div>

                <div class="skill-stat-value">
                    {int(total)}
                </div>

                <div class="skill-stat-subtitle">
                    Skills detected in your resume
                </div>

            </div>


            <div class="skill-stat-card">

                <div class="skill-stat-label">
                    Validated
                </div>

                <div class="skill-stat-value">
                    {len(validated)}
                </div>

                <div class="skill-stat-subtitle">
                    Supported by resume evidence
                </div>

            </div>


            <div class="skill-stat-card">

                <div class="skill-stat-label">
                    Validation Rate
                </div>

                <div class="skill-stat-value validation">
                    {pct:.0f}%
                </div>

                <div class="skill-stat-subtitle">
                    Skills backed by evidence
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # PROGRESS BAR
    # ========================================================

    st.html(
        f"""
        <div class="validation-progress-wrapper">

            <div class="validation-progress-top">

                <span class="validation-progress-label">
                    Skill evidence coverage
                </span>

                <span class="validation-progress-value">
                    {pct:.0f}%
                </span>

            </div>

            <div class="validation-progress">

                <div
                    class="validation-progress-fill"
                    style="width: {pct:.1f}%;">
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # VALIDATED SKILLS
    # ========================================================

    if validated:

        with st.expander(
            f"✅  Validated skills ({len(validated)})",
            expanded=False,
        ):

            for entry in validated:

                if not isinstance(entry, dict):
                    continue

                skill = str(
                    entry.get("skill", "?")
                )

                projects = (
                    entry.get("projects", [])
                    or []
                )

                similarity = entry.get(
                    "similarity"
                )

                project_text = (
                    ", ".join(
                        str(project)
                        for project in projects[:3]
                    )
                    if projects
                    else "experience section"
                )

                similarity_html = ""

                if isinstance(
                    similarity,
                    (int, float),
                ):

                    similarity_pct = (
                        float(similarity) * 100
                    )

                    similarity_html = (
                        f"""
                        <span class="skill-match">
                            {similarity_pct:.0f}% match
                        </span>
                        """
                    )

                safe_skill = escape(skill)

                safe_project_text = escape(
                    project_text
                )

                st.html(
                    f"""
                    <div class="skill-list-item">

                        <div class="skill-name">
                            ✓ {safe_skill}
                        </div>

                        <div class="skill-detail">

                            Demonstrated in:

                            <strong>
                                {safe_project_text}
                            </strong>

                            {
                                " · " + similarity_html
                                if similarity_html
                                else ""
                            }

                        </div>

                    </div>
                    """
                )


    # ========================================================
    # UNVALIDATED SKILLS
    # ========================================================

    if unvalidated:

        with st.expander(
            f"⚠️  Unvalidated skills ({len(unvalidated)})",
            expanded=False,
        ):

            st.html(
                """
                <div class="skill-description">

                    These skills are listed on your resume but
                    were not sufficiently tied to a project,
                    experience bullet, or other supporting evidence.

                </div>
                """
            )

            for skill in unvalidated:

                safe_skill = escape(
                    str(skill)
                )

                st.html(
                    f"""
                    <div class="skill-list-item">

                        <div class="skill-name">
                            ⚠ {safe_skill}
                        </div>

                        <div class="skill-detail">
                            No supporting evidence was detected.
                        </div>

                    </div>
                    """
                )