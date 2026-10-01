from html import escape
from typing import Any, Dict

import streamlit as st


def display_recommendations(
    analysis: Dict[str, Any],
) -> None:
    """
    Display high-level AI recommendations.

    Recommendations come from the backend `suggestions` field.
    Concrete action items are handled separately by action_items.py.
    """

    suggestions = analysis.get("suggestions") or []

    if not suggestions:
        return

    # The main section heading is intentionally NOT rendered here.
    # dashboard.py already renders:
    #
    # AI RECOMMENDATIONS
    # Recommended improvements
    #
    # This component only renders the recommendation cards.

    for index, suggestion in enumerate(
        suggestions,
        start=1,
    ):
        if not suggestion:
            continue

        safe_suggestion = escape(str(suggestion))

        st.html(
            f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 14px;
                background: linear-gradient(
                    135deg,
                    #111827 0%,
                    #0f172a 100%
                );
                border: 1px solid #243047;
                border-radius: 14px;
                padding: 15px 17px;
                margin: 9px 0;
                box-shadow: 0 4px 14px rgba(0,0,0,0.15);
            ">

                <div style="
                    min-width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 9px;
                    background: rgba(99,102,241,0.14);
                    border: 1px solid rgba(129,140,248,0.25);
                    color: #a5b4fc;
                    font-size: 0.8rem;
                    font-weight: 700;
                ">
                    {index}
                </div>

                <div style="
                    color: #e2e8f0;
                    font-size: 0.95rem;
                    line-height: 1.55;
                    padding-top: 4px;
                ">
                    {safe_suggestion}
                </div>

            </div>
            """
        )