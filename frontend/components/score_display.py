from typing import Any, Dict
from html import escape

import streamlit as st

from frontend.components._helpers import get_score_color, get_score_emoji


# ============================================================
# COMPONENT CONFIGURATION
# ============================================================

COMPONENTS = [
    ("Formatting", "formatting", 20, "📝"),
    ("Keywords & Skills", "keywords", 25, "🔑"),
    ("Content Quality", "content", 25, "📄"),
    ("Skill Validation", "skill_validation", 15, "✅"),
    ("ATS Compatibility", "ats_compatibility", 15, "🤖"),
]


# ============================================================
# HELPERS
# ============================================================

def _get_percentage(value: float, maximum: float) -> float:
    if maximum <= 0:
        return 0.0

    return max(0.0, min(100.0, (value / maximum) * 100))


def _get_progress_class(percentage: float) -> str:
    if percentage >= 80:
        return "score-high"
    elif percentage >= 60:
        return "score-medium"
    return "score-low"


# ============================================================
# OVERALL ATS SCORE
# ============================================================

def display_overall_score(analysis: Dict[str, Any]) -> None:
    """
    Display the main ATS score in a prominent HireMind AI card.
    """

    score = float(
        analysis.get(
            "ATS_score",
            analysis.get("ats_score", 0)
        )
    )

    score = max(0.0, min(100.0, score))

    interpretation = str(
        analysis.get("interpretation", "")
    ).strip()

    text_color, bg_color = get_score_color(score)
    emoji = get_score_emoji(score)

    safe_interpretation = escape(interpretation)

    st.html(
        f"""
        <style>

        .ats-score-section {{
            margin: 0.5rem 0 2.5rem 0;
        }}

        .ats-score-heading {{
            color: #f8fafc;
            font-size: 1.05rem;
            font-weight: 750;
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
        }}

        .ats-score-card {{
            position: relative;
            overflow: hidden;
            padding: 2.5rem 2rem;
            border-radius: 24px;

            background:
                radial-gradient(
                    circle at 50% -20%,
                    rgba(139, 92, 246, 0.22),
                    transparent 48%
                ),
                linear-gradient(
                    145deg,
                    #111827,
                    #0b1020
                );

            border: 1px solid rgba(139, 92, 246, 0.20);

            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.30),
                inset 0 1px 0 rgba(255, 255, 255, 0.035);

            text-align: center;
        }}

        .ats-score-glow {{
            position: absolute;
            width: 180px;
            height: 180px;
            left: 50%;
            top: -90px;
            transform: translateX(-50%);

            background: rgba(124, 58, 237, 0.20);
            filter: blur(55px);
            border-radius: 50%;
            pointer-events: none;
        }}

        .ats-score-value {{
            position: relative;
            color: {text_color};

            font-size: clamp(4.2rem, 8vw, 6.5rem);
            line-height: 1;
            font-weight: 850;
            letter-spacing: -0.07em;

            margin: 0;
            text-shadow:
                0 0 35px rgba(139, 92, 246, 0.25);
        }}

        .ats-score-value .score-emoji {{
            font-size: 2.2rem;
            vertical-align: 25%;
            margin-right: 0.25rem;
            letter-spacing: normal;
        }}

        .ats-score-label {{
            position: relative;

            margin-top: 0.8rem;

            color: #f8fafc;
            font-size: 1rem;
            font-weight: 750;
            letter-spacing: 0.01em;
        }}

        .ats-score-scale {{
            position: relative;

            margin-top: 0.25rem;

            color: #64748b;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .ats-score-interpretation {{
            position: relative;

            max-width: 680px;
            margin: 1.15rem auto 0;

            color: #94a3b8;
            font-size: 0.86rem;
            line-height: 1.6;
        }}

        .ats-score-line {{
            position: relative;

            width: 100%;
            max-width: 620px;
            height: 6px;

            margin: 1.5rem auto 0;

            border-radius: 999px;

            background: rgba(255, 255, 255, 0.07);
            overflow: hidden;
        }}

        .ats-score-line-fill {{
            height: 100%;
            width: {score}%;

            border-radius: inherit;

            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #8b5cf6,
                    #a855f7
                );

            box-shadow:
                0 0 18px rgba(139, 92, 246, 0.45);

            transition: width 0.6s ease;
        }}

        </style>

        <div class="ats-score-section">

            <div class="ats-score-heading">
                📊 Analysis Results
            </div>

            <div class="ats-score-card">

                <div class="ats-score-glow"></div>

                <div class="ats-score-value">
                    <span class="score-emoji">{emoji}</span>
                    {score:.0f}
                </div>

                <div class="ats-score-label">
                    Overall ATS Score
                </div>

                <div class="ats-score-scale">
                    Score out of 100
                </div>

                <div class="ats-score-line">
                    <div class="ats-score-line-fill"></div>
                </div>

                <div class="ats-score-interpretation">
                    {safe_interpretation}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# SCORE BREAKDOWN
# ============================================================

def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    """
    Display the five ATS scoring components with prominent
    values and modern progress bars.
    """

    component_scores = analysis.get("component_scores") or {}

    st.html(
        """
        <style>

        .breakdown-header {
            margin: 0.5rem 0 1.2rem 0;
        }

        .breakdown-title {
            color: #f8fafc;
            font-size: 1.15rem;
            font-weight: 800;
            margin: 0;
        }

        .breakdown-description {
            color: #64748b;
            font-size: 0.78rem;
            margin-top: 0.3rem;
        }

        .score-card {
            padding: 1.25rem;
            margin-bottom: 1rem;

            border-radius: 17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(17, 24, 39, 0.96),
                    rgba(10, 15, 28, 0.96)
                );

            border: 1px solid rgba(148, 163, 184, 0.10);

            box-shadow:
                0 8px 25px rgba(0, 0, 0, 0.16);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }

        .score-card:hover {
            transform: translateY(-2px);
            border-color: rgba(139, 92, 246, 0.30);
        }

        .score-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.85rem;
        }

        .score-card-name {
            display: flex;
            align-items: center;
            gap: 0.5rem;

            color: #e2e8f0;
            font-size: 0.86rem;
            font-weight: 700;
        }

        .score-card-icon {
            font-size: 1rem;
        }

        .score-card-number {
            color: #f8fafc;
            font-size: 1rem;
            font-weight: 850;
            letter-spacing: -0.02em;
        }

        .score-card-number .max {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .score-card-percent {
            margin-top: 0.18rem;
            color: #a78bfa;
            font-size: 0.70rem;
            font-weight: 700;
            text-align: right;
        }

        .score-progress {
            width: 100%;
            height: 7px;

            border-radius: 999px;

            background: rgba(255, 255, 255, 0.065);

            overflow: hidden;
        }

        .score-progress-fill {
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
                0 0 12px rgba(139, 92, 246, 0.30);

            transition: width 0.5s ease;
        }

        .score-progress-fill.score-medium {
            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #818cf8
                );
        }

        .score-progress-fill.score-low {
            background:
                linear-gradient(
                    90deg,
                    #475569,
                    #6366f1
                );
        }

        </style>
        """
    )

    st.html(
        """
        <div class="breakdown-header">
            <div class="breakdown-title">
                📈 Score Breakdown
            </div>

            <div class="breakdown-description">
                See how each scoring dimension contributes to your ATS performance.
            </div>
        </div>
        """
    )

    left, right = st.columns(2, gap="medium")

    for i, (label, key, max_score, icon) in enumerate(COMPONENTS):

        value = float(component_scores.get(key, 0))

        # Prevent invalid backend values from breaking the UI.
        value = max(0.0, min(float(max_score), value))

        percentage = _get_percentage(value, float(max_score))
        progress_class = _get_progress_class(percentage)

        safe_label = escape(label)

        card_html = f"""
        <div class="score-card">

            <div class="score-card-top">

                <div class="score-card-name">
                    <span class="score-card-icon">{icon}</span>
                    <span>{safe_label}</span>
                </div>

                <div>
                    <div class="score-card-number">
                        {value:.0f}
                        <span class="max">/ {max_score}</span>
                    </div>

                    <div class="score-card-percent">
                        {percentage:.0f}%
                    </div>
                </div>

            </div>

            <div class="score-progress">
                <div
                    class="score-progress-fill {progress_class}"
                    style="width: {percentage:.1f}%;">
                </div>
            </div>

        </div>
        """

        with left if i % 2 == 0 else right:
            st.html(card_html)