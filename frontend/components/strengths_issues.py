from html import escape
from typing import Any, Dict, List

import streamlit as st


def _render_strength_card(item: str) -> None:
    text = escape(str(item))

    st.html(
        f"""
        <div style="
            background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
            border: 1px solid #243047;
            border-radius: 14px;
            padding: 14px 16px;
            margin: 8px 0;
            color: #f8fafc;
            box-shadow: 0 4px 14px rgba(0,0,0,0.18);
        ">
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 12px;
                font-size: 0.95rem;
                line-height: 1.55;
            ">
                <span style="
                    min-width: 26px;
                    height: 26px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    background: rgba(34,197,94,0.14);
                    color: #4ade80;
                    font-size: 14px;
                    font-weight: 700;
                ">✓</span>

                <span style="color: #e2e8f0;">{text}</span>
            </div>
        </div>
        """
    )


def display_strengths(strengths: List[str]) -> None:
    st.html(
        """
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 18px 0 12px 0;
        ">
            <span style="font-size: 22px;">💪</span>
            <span style="
                color: #f8fafc;
                font-size: 1.35rem;
                font-weight: 700;
            ">Strengths</span>
        </div>
        """
    )

    if not strengths:
        st.html(
            """
            <div style="
                background: #111827;
                border: 1px solid #243047;
                border-radius: 14px;
                padding: 16px;
                color: #94a3b8;
                text-align: center;
                margin: 8px 0 16px 0;
            ">
                Keep improving your resume to unlock strengths!
            </div>
            """
        )
        return

    for item in strengths:
        _render_strength_card(item)


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary = analysis.get("issues_summary") or []

    if not critical and not summary:
        st.html(
            """
            <div style="
                background: linear-gradient(
                    135deg,
                    rgba(34,197,94,0.12),
                    rgba(15,23,42,0.95)
                );
                border: 1px solid rgba(74,222,128,0.28);
                border-radius: 16px;
                padding: 20px;
                margin: 20px 0;
            ">
                <div style="
                    color: #4ade80;
                    font-size: 1.15rem;
                    font-weight: 700;
                    margin-bottom: 8px;
                ">
                    ✅ No Critical Issues Found!
                </div>

                <div style="
                    color: #cbd5e1;
                    font-size: 0.95rem;
                    line-height: 1.5;
                ">
                    Your resume doesn't have any urgent issues. Nice work.
                </div>
            </div>
            """
        )
        return

    st.html(
        """
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 24px 0 8px 0;
        ">
            <span style="font-size: 22px;">🚨</span>
            <span style="
                color: #f8fafc;
                font-size: 1.35rem;
                font-weight: 700;
            ">Critical Issues</span>
        </div>

        <div style="
            color: #94a3b8;
            font-size: 0.9rem;
            margin-bottom: 14px;
        ">
            These issues should be addressed first for better ATS performance.
        </div>
        """
    )

    for item in critical:
        text = escape(str(item))

        st.html(
            f"""
            <div style="
                background: linear-gradient(135deg, #1a1114 0%, #111827 100%);
                border: 1px solid rgba(248,113,113,0.25);
                border-left: 4px solid #f87171;
                border-radius: 12px;
                padding: 13px 16px;
                margin: 8px 0;
                color: #fecaca;
                font-size: 0.94rem;
                line-height: 1.5;
            ">
                <span style="color: #f87171; margin-right: 8px;">●</span>
                {text}
            </div>
            """
        )

    extra = [s for s in summary if s not in critical]

    if extra:
        with st.expander("📋 Additional flagged items", expanded=False):
            for item in extra:
                text = escape(str(item))

                st.html(
                    f"""
                    <div style="
                        display: flex;
                        gap: 10px;
                        padding: 9px 0;
                        color: #cbd5e1;
                        font-size: 0.92rem;
                        line-height: 1.45;
                        border-bottom: 1px solid #1e293b;
                    ">
                        <span style="color: #f59e0b;">•</span>
                        <span>{text}</span>
                    </div>
                    """
                )