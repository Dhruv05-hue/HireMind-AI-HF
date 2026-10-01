from html import escape
from typing import Any, Dict, List, Tuple

import streamlit as st


SEVERITY_RANK = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

SEVERITY_STYLES = {
    "critical": {
        "icon": "🔴",
        "label": "Critical",
        "color": "#f87171",
        "background": "rgba(248,113,113,0.08)",
        "border": "rgba(248,113,113,0.28)",
    },
    "high": {
        "icon": "🟠",
        "label": "High",
        "color": "#fb923c",
        "background": "rgba(251,146,60,0.08)",
        "border": "rgba(251,146,60,0.28)",
    },
    "medium": {
        "icon": "🟡",
        "label": "Medium",
        "color": "#facc15",
        "background": "rgba(250,204,21,0.07)",
        "border": "rgba(250,204,21,0.25)",
    },
    "low": {
        "icon": "🟢",
        "label": "Low",
        "color": "#4ade80",
        "background": "rgba(74,222,128,0.07)",
        "border": "rgba(74,222,128,0.25)",
    },
}


def _collect_action_items(
    analysis: Dict[str, Any],
) -> List[Tuple[str, str, str]]:
    """
    Collect only concrete action items.

    Priority:
    1. Action items explicitly returned inside detailed feedback.
    2. Missing JD keywords / skills gaps are converted into concrete
       actions when no detailed action items exist.

    Suggestions are intentionally NOT used here because they belong
    to the Recommendations section.
    """

    items: List[Tuple[str, str, str]] = []
    seen = set()

    # ---------------------------------------------------------
    # 1. Use concrete actions from detailed feedback
    # ---------------------------------------------------------
    for issue in analysis.get("detailed_feedback") or []:
        if not isinstance(issue, dict):
            continue

        level = str(
            issue.get("severity_level") or "medium"
        ).lower()

        if level not in SEVERITY_STYLES:
            level = "medium"

        title = str(
            issue.get("issue_title") or "Resume improvement"
        ).strip()

        for action in issue.get("action_items") or []:
            if not action:
                continue

            action_text = str(action).strip()

            if not action_text:
                continue

            key = action_text.lower()

            if key in seen:
                continue

            seen.add(key)
            items.append(
                (
                    level,
                    title,
                    action_text,
                )
            )

    # ---------------------------------------------------------
    # 2. If detailed feedback has no actions, use missing
    #    keywords / skill gaps as concrete actions.
    #
    #    Do NOT use `suggestions` here because those are shown
    #    separately as AI Recommendations.
    # ---------------------------------------------------------
    if not items:

        missing = []

        for value in (
            analysis.get("missing_keywords") or [],
            (analysis.get("jd_comparison") or {}).get(
                "missing_keywords"
            )
            if isinstance(analysis.get("jd_comparison"), dict)
            else [],
            (analysis.get("jd_comparison") or {}).get(
                "skills_gap"
            )
            if isinstance(analysis.get("jd_comparison"), dict)
            else [],
        ):
            if isinstance(value, list):
                missing.extend(value)

        for keyword in missing:
            if not keyword:
                continue

            keyword = str(keyword).strip()

            if not keyword:
                continue

            key = keyword.lower()

            if key in seen:
                continue

            seen.add(key)

            items.append(
                (
                    "medium",
                    "Job Description Match",
                    (
                        f"Add '{keyword}' to your resume only if "
                        f"it accurately reflects your experience."
                    ),
                )
            )

    # ---------------------------------------------------------
    # Sort by severity
    # ---------------------------------------------------------
    items.sort(
        key=lambda row: SEVERITY_RANK.get(
            row[0],
            SEVERITY_RANK["medium"],
        )
    )

    return items


def _render_action_item(
    level: str,
    source: str,
    action: str,
    index: int,
) -> None:

    style = SEVERITY_STYLES.get(
        level,
        SEVERITY_STYLES["medium"],
    )

    safe_source = escape(str(source))
    safe_action = escape(str(action))
    safe_label = escape(style["label"])

    st.html(
        f"""
        <div style="
            background: linear-gradient(
                135deg,
                {style["background"]},
                rgba(15,23,42,0.96)
            );
            border: 1px solid {style["border"]};
            border-left: 4px solid {style["color"]};
            border-radius: 14px;
            padding: 15px 17px;
            margin: 9px 0;
            box-shadow: 0 4px 14px rgba(0,0,0,0.15);
        ">

            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 9px;
            ">

                <div style="
                    display: flex;
                    align-items: center;
                    gap: 9px;
                    color: #f8fafc;
                    font-size: 0.9rem;
                    font-weight: 650;
                ">
                    <span style="
                        font-size: 16px;
                    ">
                        {style["icon"]}
                    </span>

                    <span>
                        Action {index}
                    </span>
                </div>

                <span style="
                    color: {style["color"]};
                    background: {style["background"]};
                    border: 1px solid {style["border"]};
                    border-radius: 999px;
                    padding: 4px 9px;
                    font-size: 0.72rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.04em;
                ">
                    {safe_label}
                </span>

            </div>

            <div style="
                color: #e2e8f0;
                font-size: 0.95rem;
                line-height: 1.55;
                margin-bottom: 9px;
            ">
                {safe_action}
            </div>

            <div style="
                color: #64748b;
                font-size: 0.78rem;
                line-height: 1.4;
            ">
                Related to:
                <span style="
                    color: #94a3b8;
                ">
                    {safe_source}
                </span>
            </div>

        </div>
        """
    )


def display_action_items(
    analysis: Dict[str, Any],
) -> None:

    items = _collect_action_items(analysis)

    if not items:
        return

    # The main section heading is intentionally NOT rendered here.
    # dashboard.py already renders:
    #
    # NEXT STEPS
    # Action items
    #
    # This function only renders the action cards.

    for index, (level, source, action) in enumerate(
        items,
        start=1,
    ):
        _render_action_item(
            level=level,
            source=source,
            action=action,
            index=index,
        )