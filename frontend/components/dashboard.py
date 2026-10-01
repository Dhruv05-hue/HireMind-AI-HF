from typing import Any, Dict

import streamlit as st

from frontend.components.score_display import (
    display_overall_score,
    display_score_breakdown,
)

from frontend.components.strengths_issues import (
    display_strengths,
    display_critical_issues,
)

from frontend.components.skill_validation import (
    display_skill_validation,
)

from frontend.components.jd_comparison import (
    display_jd_comparison,
)

from frontend.components.detailed_feedback import (
    display_detailed_feedback,
)

from frontend.components.action_items import (
    display_action_items,
)

from frontend.components.recommendations import (
    display_recommendations,
)


# ============================================================
# RESULTS DASHBOARD
# ============================================================

def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    """
    Render the complete resume analysis dashboard.

    The function consumes the backend AnalysisResponse dictionary
    directly and keeps all existing analysis components intact.
    """

    # ========================================================
    # GLOBAL STYLES
    # ========================================================

    st.html(
        """
        <style>

        /* ====================================================
           HEADER
           ==================================================== */

        .analysis-header {
            margin-bottom: 2rem;
            padding: 2rem 2.2rem;
            border-radius: 22px;

            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(124, 58, 237, 0.18),
                    transparent 35%
                ),
                linear-gradient(
                    145deg,
                    #111827,
                    #0f172a
                );

            border: 1px solid rgba(148, 163, 184, 0.10);

            box-shadow:
                0 20px 50px rgba(0, 0, 0, 0.20),
                inset 0 1px 0 rgba(255,255,255,0.03);
        }

        .analysis-header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
        }

        .analysis-eyebrow {
            color: #a78bfa;
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.14em;
            margin-bottom: 0.5rem;
        }

        .analysis-title {
            margin: 0;
            color: #f8fafc;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.035em;
        }

        .analysis-subtitle {
            max-width: 700px;
            margin: 0.65rem 0 0 0;
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.65;
        }

        .analysis-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;

            padding: 0.6rem 0.9rem;
            border-radius: 999px;

            color: #cbd5e1;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.12);

            font-size: 0.75rem;
            white-space: nowrap;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.7);
        }


        /* ====================================================
           SECTION HEADERS
           ==================================================== */

        .analysis-section-header {
            margin: 2.5rem 0 1rem 0;
        }

        .analysis-section-label {
            color: #a78bfa;
            font-size: 0.7rem;
            font-weight: 750;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .analysis-section-title {
            color: #f1f5f9;
            font-size: 1.35rem;
            font-weight: 750;
            margin-top: 0.25rem;
        }

        .analysis-section-description {
            color: #64748b;
            font-size: 0.82rem;
            margin-top: 0.25rem;
        }


        /* ====================================================
           DIVIDERS
           ==================================================== */

        .analysis-divider {
            height: 1px;
            background: rgba(148, 163, 184, 0.08);
            margin: 2.5rem 0;
        }


        /* ====================================================
           COMPLETION CARD
           ==================================================== */

        .analysis-completion {
            margin-top: 3rem;
            padding: 1.5rem;
            text-align: center;
            border-radius: 18px;

            background:
                linear-gradient(
                    145deg,
                    rgba(124, 58, 237, 0.10),
                    rgba(79, 70, 229, 0.05)
                );

            border: 1px solid rgba(167, 139, 250, 0.12);
        }

        .analysis-completion-title {
            color: #c4b5fd;
            font-size: 1rem;
            font-weight: 700;
        }

        .analysis-completion-text {
            color: #64748b;
            font-size: 0.8rem;
            margin-top: 0.4rem;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 768px) {

            .analysis-header {
                padding: 1.5rem;
            }

            .analysis-header-content {
                flex-direction: column;
                align-items: flex-start;
            }

            .analysis-title {
                font-size: 1.65rem;
            }

        }

        </style>
        """
    )


    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.html(
        """
        <div class="analysis-header">

            <div class="analysis-header-content">

                <div>

                    <div class="analysis-eyebrow">
                        AI RESUME ANALYSIS
                    </div>

                    <h1 class="analysis-title">
                        Resume Performance Report
                    </h1>

                    <p class="analysis-subtitle">
                        Understand how your resume performs across
                        ATS compatibility, skills, content, and
                        job-description matching.
                    </p>

                </div>

                <div class="analysis-status">
                    <span class="status-dot"></span>
                    Analysis Complete
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # OVERALL SCORE
    # ========================================================

    st.html(
        """
        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Overall Performance
            </div>

            <div class="analysis-section-title">
                Your ATS Score
            </div>

            <div class="analysis-section-description">
                A combined evaluation of your resume's ATS readiness.
            </div>

        </div>
        """
    )

    display_overall_score(analysis)


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Score Breakdown
            </div>

            <div class="analysis-section-title">
                Where your resume performs
            </div>

            <div class="analysis-section-description">
                See how each scoring dimension contributes to your
                overall ATS performance.
            </div>

        </div>
        """
    )

    display_score_breakdown(analysis)


    # ========================================================
    # STRENGTHS & CRITICAL ISSUES
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Resume Diagnosis
            </div>

            <div class="analysis-section-title">
                Strengths & areas to improve
            </div>

            <div class="analysis-section-description">
                Understand what's working and what may be
                limiting your resume performance.
            </div>

        </div>
        """
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        display_strengths(
            analysis.get("strengths") or []
        )

    with col2:
        display_critical_issues(analysis)


    # ========================================================
    # SKILL VALIDATION
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Skill Intelligence
            </div>

            <div class="analysis-section-title">
                Are your skills backed by evidence?
            </div>

            <div class="analysis-section-description">
                Skills are checked against projects and experience
                found in your resume.
            </div>

        </div>
        """
    )

    display_skill_validation(analysis)


    # ========================================================
    # JOB DESCRIPTION MATCH
    # ========================================================

    jd_comparison = (
        analysis.get("jd_comparison")
        or analysis.get("jd_match_analysis")
    )

    if jd_comparison:

        st.html(
            """
            <div class="analysis-divider"></div>

            <div class="analysis-section-header">

                <div class="analysis-section-label">
                    Job Match
                </div>

                <div class="analysis-section-title">
                    Resume vs Job Description
                </div>

                <div class="analysis-section-description">
                    Compare your resume against the target role's
                    keywords, skills, and semantic requirements.
                </div>

            </div>
            """
        )

        display_jd_comparison(jd_comparison)


    # ========================================================
    # DETAILED FEEDBACK
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Detailed Analysis
            </div>

            <div class="analysis-section-title">
                What should you improve?
            </div>

            <div class="analysis-section-description">
                Review detailed explanations of the issues detected
                in your resume.
            </div>

        </div>
        """
    )

    display_detailed_feedback(analysis)


    # ========================================================
    # ACTION ITEMS
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                Next Steps
            </div>

            <div class="analysis-section-title">
                Action items
            </div>

            <div class="analysis-section-description">
                Concrete changes you can make to improve your resume.
            </div>

        </div>
        """
    )

    display_action_items(analysis)


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.html(
        """
        <div class="analysis-divider"></div>

        <div class="analysis-section-header">

            <div class="analysis-section-label">
                AI Recommendations
            </div>

            <div class="analysis-section-title">
                Recommended improvements
            </div>

            <div class="analysis-section-description">
                Additional recommendations generated from your
                analysis results.
            </div>

        </div>
        """
    )

    display_recommendations(analysis)


    # ========================================================
    # COMPLETION MESSAGE
    # ========================================================

    st.html(
        """
        <div class="analysis-completion">

            <div class="analysis-completion-title">
                ✦ Your analysis is complete
            </div>

            <div class="analysis-completion-text">
                Use the recommendations above to make your resume
                stronger and more targeted.
            </div>

        </div>
        """
    )