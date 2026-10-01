from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score."""

    if score >= 80:
        return "#4ade80", "rgba(74, 222, 128, 0.12)"  # green

    if score >= 60:
        return "#fb923c", "rgba(251, 146, 60, 0.12)"  # orange

    return "#f87171", "rgba(248, 113, 113, 0.12)"  # red


def get_score_emoji(score: float) -> str:
    """Emoji that matches the score band — used in headlines."""

    if score >= 90:
        return "🌟"

    if score >= 80:
        return "✅"

    if score >= 70:
        return "👍"

    if score >= 60:
        return "⚠️"

    return "🔴"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """
    Return (icon, text_color, background_color) for an IssueDetail severity.
    Matches the values the backend emits in `detailed_feedback[].severity_level`.
    """

    level = (severity or "").lower()

    if level == "critical":
        return (
            "🔴",
            "#f87171",
            "rgba(248, 113, 113, 0.10)",
        )

    if level == "high":
        return (
            "🟠",
            "#fb923c",
            "rgba(251, 146, 60, 0.10)",
        )

    if level == "medium":
        return (
            "🟡",
            "#facc15",
            "rgba(250, 204, 21, 0.08)",
        )

    return (
        "🟢",
        "#4ade80",
        "rgba(74, 222, 128, 0.08)",
    )