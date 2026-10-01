from typing import Any, Dict, List
from html import escape

import streamlit as st

from frontend.components._helpers import get_severity_style


SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def _group_by_severity(
    issues: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:

    grouped: Dict[str, List[Dict[str, Any]]] = {
        level: []
        for level in SEVERITY_ORDER
    }

    for issue in issues:

        if not isinstance(issue, dict):
            continue

        level = str(
            issue.get("severity_level") or "low"
        ).lower().strip()

        if level not in grouped:
            level = "low"

        grouped[level].append(issue)

    return grouped


def _safe_text(value: Any) -> str:
    if value is None:
        return ""

    return escape(str(value))


def _render_issue(
    issue: Dict[str, Any],
    issue_number: int,
) -> None:

    severity = str(
        issue.get("severity_level") or "low"
    ).lower()

    icon, text_color, bg_color = get_severity_style(
        severity
    )

    title = _safe_text(
        issue.get(
            "issue_title",
            "Untitled issue"
        )
    )

    impact = _safe_text(
        issue.get("ats_impact", "")
    )

    explanation = _safe_text(
        issue.get("explanation", "")
    )

    where = _safe_text(
        issue.get("where_it_appears", "")
    )

    how_to_fix = _safe_text(
        issue.get("how_to_fix", "")
    )

    action_items = (
        issue.get("action_items") or []
    )

    example = _safe_text(
        issue.get("example_improvement", "")
    )

    severity_label = escape(
        severity.title()
    )

    # ========================================================
    # ISSUE SUMMARY CARD
    # ========================================================

    st.html(
        f"""
        <style>

        .feedback-card {{
            position: relative;

            margin: 0.8rem 0;

            padding: 1.35rem 1.4rem;

            border-radius: 17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17, 24, 39, 0.98),
                    rgba(10, 15, 28, 0.98)
                );

            border: 1px solid
                rgba(148, 163, 184, 0.11);

            border-left:
                4px solid {text_color};

            box-shadow:
                0 10px 30px
                rgba(0, 0, 0, 0.18);
        }}


        .feedback-card-top {{
            display: flex;

            justify-content: space-between;
            align-items: flex-start;

            gap: 1rem;
        }}


        .feedback-card-number {{
            color: #64748b;

            font-size: 0.68rem;
            font-weight: 750;

            letter-spacing: 0.08em;
            text-transform: uppercase;

            margin-bottom: 0.35rem;
        }}


        .feedback-card-title {{
            color: #f8fafc;

            font-size: 1rem;
            font-weight: 800;

            line-height: 1.4;
        }}


        .feedback-severity {{
            flex-shrink: 0;

            padding: 0.35rem 0.65rem;

            border-radius: 999px;

            color: {text_color};

            background: {bg_color};

            border: 1px solid
                rgba(255, 255, 255, 0.08);

            font-size: 0.66rem;
            font-weight: 800;

            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}


        .feedback-impact {{
            margin-top: 0.85rem;

            padding: 0.75rem 0.85rem;

            border-radius: 10px;

            background:
                rgba(255, 255, 255, 0.035);

            color: #cbd5e1;

            font-size: 0.78rem;

            line-height: 1.5;
        }}


        .feedback-impact-label {{
            color: #a78bfa;

            font-size: 0.65rem;
            font-weight: 800;

            letter-spacing: 0.07em;
            text-transform: uppercase;

            margin-right: 0.4rem;
        }}

        </style>


        <div class="feedback-card">

            <div class="feedback-card-top">

                <div>

                    <div class="feedback-card-number">
                        Issue {issue_number}
                    </div>

                    <div class="feedback-card-title">
                        {icon} {title}
                    </div>

                </div>

                <div class="feedback-severity">
                    {severity_label}
                </div>

            </div>


            {
                f'''
                <div class="feedback-impact">
                    <span class="feedback-impact-label">
                        ATS Impact
                    </span>
                    {impact}
                </div>
                '''
                if impact
                else ""
            }

        </div>
        """
    )


    # ========================================================
    # DETAILED ISSUE INFORMATION
    # ========================================================

    has_details = any(
        [
            explanation,
            where,
            how_to_fix,
            action_items,
            example,
        ]
    )

    if not has_details:
        return


    with st.expander(
        "View issue details",
        expanded=False,
    ):

        # ----------------------------------------------------
        # WHAT IS HAPPENING
        # ----------------------------------------------------

        if explanation:

            st.html(
                f"""
                <div class="detail-section">

                    <div class="detail-label">
                        🔎 WHAT'S HAPPENING
                    </div>

                    <div class="detail-text">
                        {explanation}
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # WHERE IT APPEARS
        # ----------------------------------------------------

        if where:

            st.html(
                f"""
                <div class="detail-section">

                    <div class="detail-label">
                        📍 WHERE IT APPEARS
                    </div>

                    <div class="detail-text">
                        {where}
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # HOW TO FIX
        # ----------------------------------------------------

        if how_to_fix:

            st.html(
                f"""
                <div class="fix-card">

                    <div class="fix-title">
                        🛠️ HOW TO FIX IT
                    </div>

                    <div class="fix-text">
                        {how_to_fix}
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # ACTION ITEMS
        # ----------------------------------------------------

        if action_items:

            st.html(
                """
                <div class="detail-section">

                    <div class="detail-label">
                        ✓ ACTION ITEMS
                    </div>

                </div>
                """
            )

            for item in action_items:

                safe_item = _safe_text(item)

                st.html(
                    f"""
                    <div class="action-item">

                        <span class="action-check">
                            ✓
                        </span>

                        <span class="action-text">
                            {safe_item}
                        </span>

                    </div>
                    """
                )


        # ----------------------------------------------------
        # EXAMPLE IMPROVEMENT
        # ----------------------------------------------------

        if example:

            st.html(
                """
                <div class="detail-label example-label">
                    ✨ EXAMPLE IMPROVEMENT
                </div>
                """
            )

            st.code(
                example,
                language="text",
            )


def display_detailed_feedback(
    analysis: Dict[str, Any]
) -> None:

    issues = (
        analysis.get("detailed_feedback") or []
    )

    if not issues:

        st.html(
            """
            <style>

            .feedback-empty {{
                padding: 1.5rem;

                border-radius: 16px;

                background:
                    rgba(17, 24, 39, 0.75);

                border:
                    1px solid
                    rgba(148, 163, 184, 0.10);

                color: #94a3b8;

                text-align: center;
            }}

            .feedback-empty-title {{
                color: #f8fafc;

                font-size: 0.95rem;
                font-weight: 750;

                margin-bottom: 0.35rem;
            }}

            .feedback-empty-text {{
                font-size: 0.78rem;
            }}

            </style>

            <div class="feedback-empty">

                <div class="feedback-empty-title">
                    ✓ No detailed issues detected
                </div>

                <div class="feedback-empty-text">
                    Your analysis did not produce any
                    per-issue feedback for this resume.
                </div>

            </div>
            """
        )

        return


    # ========================================================
    # GLOBAL STYLES
    # ========================================================

    st.html(
        """
        <style>

        .feedback-header {
            margin-bottom: 1.5rem;
        }


        .feedback-eyebrow {
            color: #a78bfa;

            font-size: 0.68rem;
            font-weight: 800;

            letter-spacing: 0.10em;
            text-transform: uppercase;

            margin-bottom: 0.4rem;
        }


        .feedback-title {
            color: #f8fafc;

            font-size: 1.45rem;
            font-weight: 850;

            letter-spacing: -0.025em;

            margin: 0;
        }


        .feedback-description {
            color: #64748b;

            font-size: 0.78rem;

            line-height: 1.55;

            margin-top: 0.4rem;
        }


        .severity-heading {
            display: flex;

            align-items: center;
            gap: 0.55rem;

            margin-top: 1.5rem;
            margin-bottom: 0.6rem;
        }


        .severity-heading-title {
            color: #e2e8f0;

            font-size: 0.86rem;
            font-weight: 800;
        }


        .severity-count {
            color: #64748b;

            font-size: 0.7rem;
            font-weight: 650;
        }


        .detail-section {
            margin:
                0 0 1.25rem 0;
        }


        .detail-label {
            color: #a78bfa;

            font-size: 0.67rem;
            font-weight: 800;

            letter-spacing: 0.08em;

            margin-bottom: 0.45rem;
        }


        .detail-text {
            color: #cbd5e1;

            font-size: 0.82rem;

            line-height: 1.65;
        }


        .fix-card {
            margin:
                0.25rem 0 1.25rem 0;

            padding: 1rem 1.05rem;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    rgba(99, 102, 241, 0.10),
                    rgba(139, 92, 246, 0.06)
                );

            border:
                1px solid
                rgba(139, 92, 246, 0.18);
        }


        .fix-title {
            color: #c4b5fd;

            font-size: 0.68rem;
            font-weight: 800;

            letter-spacing: 0.08em;

            margin-bottom: 0.45rem;
        }


        .fix-text {
            color: #e2e8f0;

            font-size: 0.82rem;

            line-height: 1.65;
        }


        .action-item {
            display: flex;

            align-items: flex-start;

            gap: 0.65rem;

            margin-bottom: 0.55rem;

            padding:
                0.65rem 0.75rem;

            border-radius: 10px;

            background:
                rgba(255, 255, 255, 0.025);

            border:
                1px solid
                rgba(148, 163, 184, 0.07);
        }


        .action-check {
            flex-shrink: 0;

            display: flex;

            align-items: center;
            justify-content: center;

            width: 19px;
            height: 19px;

            border-radius: 50%;

            background:
                rgba(16, 185, 129, 0.14);

            color: #6ee7b7;

            font-size: 0.65rem;
            font-weight: 800;
        }


        .action-text {
            color: #cbd5e1;

            font-size: 0.78rem;

            line-height: 1.5;
        }


        .example-label {
            margin-top: 1.25rem;
        }

        </style>
        """
    )


    # ========================================================
    # HEADER
    # ========================================================

    # ========================================================
    # GROUP ISSUES
    # ========================================================

    grouped = _group_by_severity(issues)

    issue_number = 1

    for level in SEVERITY_ORDER:

        items = grouped.get(level, [])

        if not items:
            continue

        icon, text_color, bg_color = get_severity_style(
            level
        )

        safe_level = escape(
            level.title()
        )

        st.html(
            f"""
            <div class="severity-heading">

                <span>
                    {icon}
                </span>

                <span class="severity-heading-title"
                      style="color:{text_color};">

                    {safe_level} Issues

                </span>

                <span class="severity-count">
                    ({len(items)})
                </span>

            </div>
            """
        )

        for issue in items:

            _render_issue(
                issue,
                issue_number,
            )

            issue_number += 1