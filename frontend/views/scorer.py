from typing import Optional

import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


# ============================================================
# CONFIG
# ============================================================

MAX_FILE_SIZE_MB = 5


# ============================================================
# NAVIGATION
# ============================================================

def _navigate(view: str) -> None:
    st.session_state["current_view"] = view
    st.rerun()


# ============================================================
# CSS
# ============================================================

def _inject_scorer_css() -> None:

    st.html(
        """
        <style>

        /* ====================================================
           GLOBAL PAGE
           ==================================================== */

        html,
        body {
            background: #070a13 !important;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(99,102,241,0.10),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 8%,
                    rgba(139,92,246,0.10),
                    transparent 30%
                ),
                linear-gradient(
                    180deg,
                    #090c18 0%,
                    #060810 100%
                ) !important;

            color: #ffffff !important;
        }


        /* ====================================================
           STREAMLIT HEADER
           ==================================================== */

        [data-testid="stHeader"] {
            height: 0 !important;
            min-height: 0 !important;
            background: transparent !important;
            border: none !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        #MainMenu {
            visibility: hidden !important;
        }

        footer {
            visibility: hidden !important;
        }


        /* ====================================================
           MAIN CONTAINER
           ==================================================== */

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stMain"] {
            background: transparent !important;
        }

        .main {
            background: transparent !important;
        }

        .block-container {
            max-width: 1250px !important;
            padding-top: 0.8rem !important;
            padding-bottom: 4rem !important;
        }


        /* ====================================================
           SIDEBAR — BRIGHT TEXT
           ==================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0d1120 0%,
                    #080b15 100%
                ) !important;

            border-right:
                1px solid
                rgba(255,255,255,0.10) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }


        /* ALL SIDEBAR TEXT */

        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label {

            opacity: 1 !important;
        }


        /* Sidebar normal text */

        [data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"] p {

            color:
                #cbd1e1 !important;

            font-size:
                13px !important;
        }


        /* Sidebar headings */

        [data-testid="stSidebar"]
        h1,
        [data-testid="stSidebar"]
        h2,
        [data-testid="stSidebar"]
        h3,
        [data-testid="stSidebar"]
        h4 {

            color:
                #f3f4f8 !important;

            opacity:
                1 !important;
        }


        /* Sidebar section labels */

        [data-testid="stSidebar"]
        .sidebar-section-title {

            color:
                #aeb7cc !important;

            opacity:
                1 !important;

            font-size:
                11px !important;

            font-weight:
                800 !important;

            letter-spacing:
                1.2px !important;
        }


        /* Sidebar brand */

        [data-testid="stSidebar"]
        .brand-name {

            color:
                #ffffff !important;

            font-size:
                14px !important;

            font-weight:
                750 !important;
        }


        [data-testid="stSidebar"]
        .brand-subtitle {

            color:
                #9da7bd !important;

            font-size:
                11px !important;
        }


        /* Sidebar user information */

        [data-testid="stSidebar"]
        .sidebar-user-label {

            color:
                #9ca6bc !important;

            font-size:
                10px !important;

            font-weight:
                600 !important;
        }


        [data-testid="stSidebar"]
        .sidebar-user-email {

            color:
                #e0e4ef !important;

            font-size:
                12px !important;

            font-weight:
                600 !important;

            word-break:
                break-word !important;
        }


        /* Sidebar navigation buttons */

        [data-testid="stSidebar"]
        .stButton > button {

            width:
                100% !important;

            min-height:
                43px !important;

            border-radius:
                11px !important;

            background:
                rgba(255,255,255,0.035) !important;

            color:
                #dce1ed !important;

            border:
                1px solid
                rgba(255,255,255,0.11) !important;

            font-weight:
                600 !important;

            opacity:
                1 !important;

            transition:
                all 0.18s ease !important;
        }


        [data-testid="stSidebar"]
        .stButton > button:hover {

            background:
                rgba(99,102,241,0.16) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(129,140,248,0.42) !important;

            transform:
                translateY(-1px) !important;
        }


        /* Sidebar divider */

        [data-testid="stSidebar"]
        .sidebar-divider {

            background:
                rgba(255,255,255,0.09) !important;

            height:
                1px !important;
        }


        /* ====================================================
           PAGE HEADER
           ==================================================== */

        .scorer-hero {

            position: relative;

            overflow: hidden;

            padding:
                30px 34px;

            margin-bottom:
                26px;

            border-radius:
                22px;

            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139,92,246,0.18),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 8% 90%,
                    rgba(99,102,241,0.12),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    rgba(21,26,50,0.96),
                    rgba(12,16,31,0.96)
                );

            border:
                1px solid
                rgba(255,255,255,0.075);

            box-shadow:
                0 22px 60px
                rgba(0,0,0,0.28),

                inset 0 1px 0
                rgba(255,255,255,0.035);
        }


        .scorer-eyebrow {

            color:
                #818cf8;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.6px;

            text-transform:
                uppercase;

            margin-bottom:
                10px;
        }


        .scorer-title {

            color:
                #ffffff;

            font-size:
                34px;

            font-weight:
                800;

            line-height:
                1.15;

            letter-spacing:
                -1.1px;

            margin:
                0 0 4px 0;
        }


        .scorer-title-gradient {

            color:
                #a78bfa;

            font-size:
                18px;

            font-weight:
                650;

            margin-bottom:
                12px;
        }


        .scorer-description {

            max-width:
                760px;

            color:
                #a5aec2;

            font-size:
                13px;

            line-height:
                1.7;
        }


        /* ====================================================
           MODE SELECTOR
           ==================================================== */

        .mode-card {

            padding:
                18px 20px;

            margin-bottom:
                12px;

            border-radius:
                16px;

            background:
                rgba(17,21,38,0.70);

            border:
                1px solid
                rgba(255,255,255,0.06);
        }


        .mode-label {

            color:
                #f0f2f8;

            font-size:
                13px;

            font-weight:
                700;

            margin-bottom:
                10px;
        }


        /* ====================================================
        RADIO BUTTONS — FINAL TEXT FIX
        ==================================================== */

        [data-testid="stRadio"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        [data-testid="stRadio"] > div {
            background: transparent !important;
        }


        /* Radio option */

        [data-testid="stRadio"] label {
            background: transparent !important;
            color: #d8dced !important;
            opacity: 1 !important;
        }


        /* Radio text container */

        [data-testid="stRadio"] label p,
        [data-testid="stRadio"] label span {
            color: #d8dced !important;
            opacity: 1 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }


        /* Hover */

        [data-testid="stRadio"] label:hover {
            background: rgba(99,102,241,0.10) !important;
            color: #ffffff !important;
        }

        [data-testid="stRadio"] label:hover p,
        [data-testid="stRadio"] label:hover span {
            color: #ffffff !important;
        }


        /* Selected option */

        [data-testid="stRadio"] label:has(input:checked) {
            color: #ffffff !important;
        }

        [data-testid="stRadio"] label:has(input:checked) p,
        [data-testid="stRadio"] label:has(input:checked) span {
            color: #ffffff !important;
        }

        /* ====================================================
           STEP HEADERS
           ==================================================== */

        .step-eyebrow {

            color:
                #818cf8;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.5px;

            text-transform:
                uppercase;

            margin-bottom:
                5px;
        }


        .step-title {

            color:
                #ffffff;

            font-size:
                18px;

            font-weight:
                750;

            margin-bottom:
                6px;
        }


        .step-description {

            color:
                #98a2b8;

            font-size:
                12px;

            line-height:
                1.5;

            margin-bottom:
                12px;
        }


        /* ====================================================
           FILE UPLOADER
           ==================================================== */

        [data-testid="stFileUploader"] {

            background:
                rgba(255,255,255,0.025) !important;

            border:
                1px solid
                rgba(255,255,255,0.08) !important;

            border-radius:
                13px !important;

            padding:
                8px !important;
        }


        [data-testid="stFileUploader"] section {

            background:
                transparent !important;

            border:
                none !important;
        }


        [data-testid="stFileUploaderDropzone"] {

            background:
                rgba(255,255,255,0.018) !important;

            border:
                1px dashed
                rgba(129,140,248,0.22) !important;

            border-radius:
                10px !important;
        }


        [data-testid="stFileUploaderDropzone"] div {

            color:
                #c0c7d7 !important;
        }


        [data-testid="stFileUploader"] button {

            background:
                rgba(99,102,241,0.14) !important;

            color:
                #d9dcff !important;

            border:
                1px solid
                rgba(129,140,248,0.28) !important;

            border-radius:
                9px !important;
        }


        [data-testid="stFileUploader"] button:hover {

            background:
                rgba(99,102,241,0.24) !important;

            color:
                #ffffff !important;
        }


        /* ====================================================
           TEXT AREA
           ==================================================== */

        [data-testid="stTextArea"] textarea {

            background:
                #111625 !important;

            color:
                #edf0f8 !important;

            border:
                1px solid
                rgba(255,255,255,0.10) !important;

            border-radius:
                11px !important;
        }


        [data-testid="stTextArea"] textarea:focus {

            border-color:
                rgba(129,140,248,0.55) !important;

            box-shadow:
                0 0 0 1px
                rgba(129,140,248,0.20) !important;
        }


        [data-testid="stTextArea"] textarea::placeholder {

            color:
                #7f899e !important;

            opacity:
                1 !important;
        }


        /* ====================================================
           LABELS
           ==================================================== */

        .stFileUploader label,
        .stTextArea label,
        .stTextInput label {

            color:
                #b9c1d2 !important;

            font-weight:
                600 !important;
        }


        /* ====================================================
           MAIN BUTTONS
           ==================================================== */

        .stButton > button {

            min-height:
                44px !important;

            border-radius:
                11px !important;

            font-weight:
                650 !important;

            transition:
                transform 0.2s ease,
                background 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease !important;
        }


        .stButton > button[kind="primary"] {

            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #7c3aed
                ) !important;

            color:
                #ffffff !important;

            border:
                1px solid
                rgba(167,139,250,0.60) !important;

            box-shadow:
                0 8px 25px
                rgba(99,102,241,0.20) !important;
        }


        .stButton > button[kind="primary"]:hover {

            background:
                linear-gradient(
                    135deg,
                    #7174ff,
                    #8b5cf6
                ) !important;

            color:
                #ffffff !important;

            transform:
                translateY(-2px) !important;

            box-shadow:
                0 12px 32px
                rgba(99,102,241,0.32) !important;
        }


        .stButton > button:not([kind="primary"]) {

            background:
                rgba(255,255,255,0.035) !important;

            color:
                #cbd0df !important;

            border:
                1px solid
                rgba(255,255,255,0.10) !important;
        }


        .stButton > button:not([kind="primary"]):hover {

            background:
                rgba(129,140,248,0.09) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(129,140,248,0.35) !important;

            transform:
                translateY(-2px) !important;
        }


        /* ====================================================
           DOWNLOAD BUTTONS
           ==================================================== */

        [data-testid="stDownloadButton"] button {
            width: 100% !important;
            min-height: 44px !important;
            border-radius: 11px !important;
            background: linear-gradient(135deg, #151b35, #11162a) !important;
            color: #eef2ff !important;
            border: 1px solid rgba(129,140,248,0.30) !important;
            font-weight: 700 !important;
            opacity: 1 !important;
            box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stDownloadButton"] button p,
        [data-testid="stDownloadButton"] button span {
            color: #eef2ff !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        [data-testid="stDownloadButton"] button:hover {
            background: linear-gradient(135deg, #242a52, #1b2140) !important;
            color: #ffffff !important;
            border-color: rgba(167,139,250,0.60) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 30px rgba(99,102,241,0.22) !important;
        }


        /* ====================================================
           ALERTS
           ==================================================== */

        [data-testid="stAlert"] {

            background:
                rgba(255,255,255,0.035) !important;

            border:
                1px solid
                rgba(255,255,255,0.08) !important;

            color:
                #d1d6e3 !important;
        }


        [data-testid="stAlert"] p {

            color:
                #d1d6e3 !important;
        }


        /* ====================================================
           DIVIDER
           ==================================================== */

        hr {

            border-color:
                rgba(255,255,255,0.07) !important;
        }


        /* ====================================================
           RESULTS
           ==================================================== */

        .results-header {

            margin:
                30px 0 18px 0;

            padding:
                22px 24px;

            border-radius:
                17px;

            background:
                linear-gradient(
                    135deg,
                    rgba(99,102,241,0.12),
                    rgba(139,92,246,0.07)
                );

            border:
                1px solid
                rgba(129,140,248,0.14);
        }


        .results-eyebrow {

            color:
                #818cf8;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.5px;

            text-transform:
                uppercase;

            margin-bottom:
                5px;
        }


        .results-title {

            color:
                #ffffff;

            font-size:
                23px;

            font-weight:
                800;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 900px) {

            .scorer-title {
                font-size:
                    29px;
            }

            .scorer-hero {
                padding:
                    26px 24px;
            }
        }


        @media (max-width: 700px) {

            .block-container {
                padding-left:
                    1rem !important;

                padding-right:
                    1rem !important;
            }

            .scorer-title {
                font-size:
                    26px;
            }

            .scorer-title-gradient {
                font-size:
                    16px;
            }
        }

        </style>
        """
    )

# ============================================================
# JOB DESCRIPTION READER
# ============================================================

def _read_jd(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    try:
        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="ignore",
        ).strip()
    except Exception:
        return ""


# ============================================================
# BACKEND ERROR
# ============================================================

def _show_backend_error(error) -> None:

    message = str(error)

    st.error(
        "Analysis failed. Please check that the backend is running "
        "and try again."
    )

    with st.expander("Technical details"):
        st.code(message)


# ============================================================
# SUMMARY
# ============================================================

def _summary_text(analysis: dict) -> str:

    score = analysis.get(
        "ATS_score",
        analysis.get("ats_score", 0),
    )

    interpretation = analysis.get(
        "interpretation",
        "",
    )

    if interpretation:
        return (
            f"ATS Score: {float(score):.1f}/100 — "
            f"{interpretation}"
        )

    return (
        f"ATS Score: {float(score):.1f}/100"
    )


# ============================================================
# UPLOAD AREA
# ============================================================

def _render_upload_area(
    analysis_mode: str,
):

    resume_file = None
    jd_file = None
    jd_text = ""

    st.html(
        """
        <div class="step-eyebrow">
            STEP 01
        </div>

        <div class="step-title">
            Upload your resume
        </div>

        <div class="step-description">
            Upload the resume you want HireMind AI to analyze.
        </div>
        """
    )


    resume_file = st.file_uploader(
        "Resume file",
        type=["pdf", "doc", "docx"],
        key="resume_upload",
        help=(
            f"Supported formats: PDF, DOC, DOCX. "
            f"Maximum file size: {MAX_FILE_SIZE_MB} MB."
        ),
        label_visibility="collapsed",
    )


    if resume_file is not None:

        size_mb = resume_file.size / (
            1024 * 1024
        )

        if size_mb > MAX_FILE_SIZE_MB:

            st.error(
                f"Resume is {size_mb:.2f} MB. "
                f"The maximum allowed size is "
                f"{MAX_FILE_SIZE_MB} MB."
            )

            resume_file = None

        else:

            st.success(
                f"✓ {resume_file.name} "
                f"({size_mb:.2f} MB)"
            )


    if analysis_mode == "Job Description Comparison":

        st.html(
            """
            <div style="
                height:24px;
            "></div>

            <div class="step-eyebrow">
                STEP 02 · REQUIRED
            </div>

            <div class="step-title">
                Add a job description
            </div>

            <div class="step-description">
                Compare your resume against a specific role.
            </div>
            """
        )


        jd_source = st.radio(
            "Job description source",
            [
                "Paste text",
                "Upload .txt file",
            ],
            horizontal=True,
            key="jd_source",
            label_visibility="collapsed",
        )


        if jd_source == "Paste text":

            jd_text = st.text_area(
                "Job description",
                height=220,
                placeholder=(
                    "Paste the job description here..."
                ),
                key="jd_text_input",
                label_visibility="collapsed",
            )

        else:

            jd_file = st.file_uploader(
                "Job description file",
                type=["txt"],
                key="jd_upload",
                label_visibility="collapsed",
                help="Upload a plain text job description.",
            )

            jd_text = _read_jd(jd_file)

    else:

        st.html(
            """
            <div style="
                height:24px;
            "></div>

            <div class="step-eyebrow">
                STEP 02 · OPTIONAL
            </div>

            <div class="step-title">
                Add a job description
            </div>

            <div class="step-description">
                Compare your resume against a specific role.
            </div>

            <div class="jd-card">

                <div class="jd-disabled">

                    <div class="jd-disabled-icon">
                        ✦
                    </div>

                    <div class="jd-disabled-title">
                        Target a specific job
                    </div>

                    <div class="jd-disabled-text">
                        Switch to Job Description Comparison
                        above to analyze your resume against
                        a specific position.
                    </div>

                </div>

            </div>
            """
        )


    return resume_file, jd_file, jd_text


# ============================================================
# NORMALIZE RESULT DATA FOR THE DASHBOARD
# ============================================================

def _prepare_analysis_for_dashboard(analysis: dict) -> dict:
    """
    Normalize backend analysis data for the frontend dashboard.

    Action items are stored by the backend inside detailed_feedback,
    while the dedicated frontend component expects a top-level list.
    This helper bridges those two representations without changing
    the backend response or ATS score.
    """
    if not isinstance(analysis, dict):
        return {}

    normalized = dict(analysis)

    detailed_feedback = normalized.get("detailed_feedback") or []

    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------
    existing_action_items = normalized.get("action_items") or []

    if not existing_action_items:
        collected = []
        seen = set()

        for issue in detailed_feedback:
            if not isinstance(issue, dict):
                continue

            for item in issue.get("action_items") or []:
                item = str(item).strip()
                if item and item.lower() not in seen:
                    seen.add(item.lower())
                    collected.append(item)

        normalized["action_items"] = collected

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------
    existing_suggestions = normalized.get("suggestions") or []

    if not existing_suggestions:
        recommendations = []
        seen = set()

        def add_recommendation(value: str) -> None:
            value = str(value).strip()
            if not value:
                return
            key = value.lower()
            if key not in seen:
                seen.add(key)
                recommendations.append(value)

        # Prefer backend-generated issue guidance.
        for issue in detailed_feedback:
            if not isinstance(issue, dict):
                continue

            add_recommendation(issue.get("how_to_fix", ""))

            example = str(issue.get("example_improvement") or "").strip()
            if example:
                add_recommendation(f"Use an evidence-based improvement such as: {example}")

        # Use critical issues if the backend did not provide detailed feedback.
        for issue in normalized.get("critical_issues") or []:
            add_recommendation(str(issue))

        # Use JD gaps as targeted recommendations.
        jd_comparison = (
            normalized.get("jd_comparison")
            or normalized.get("jd_match_analysis")
            or {}
        )

        for keyword in jd_comparison.get("missing_keywords") or []:
            add_recommendation(
                f"Add the job-description keyword '{keyword}' if it accurately reflects your experience."
            )

        for skill in jd_comparison.get("skills_gap") or []:
            add_recommendation(
                f"Strengthen evidence for '{skill}' through relevant projects, experience, or certifications."
            )

        # Last-resort recommendations based on the actual component scores.
        component_scores = normalized.get("component_scores") or {}

        try:
            formatting = float(component_scores.get("formatting", 0))
            if formatting < 18:
                add_recommendation(
                    "Improve resume formatting with consistent headings, spacing, dates, and ATS-readable structure."
                )
        except (TypeError, ValueError):
            pass

        try:
            keywords = float(component_scores.get("keywords", 0))
            if keywords < 22:
                add_recommendation(
                    "Strengthen keyword coverage by using relevant skills and terminology naturally throughout the resume."
                )
        except (TypeError, ValueError):
            pass

        try:
            content = float(component_scores.get("content", 0))
            if content < 22:
                add_recommendation(
                    "Improve content by turning responsibilities into concise, measurable achievement statements."
                )
        except (TypeError, ValueError):
            pass

        try:
            validation = float(component_scores.get("skill_validation", 0))
            if validation < 13:
                add_recommendation(
                    "Add project or work evidence for important skills so recruiters can verify your experience."
                )
        except (TypeError, ValueError):
            pass

        normalized["suggestions"] = recommendations[:8]

    # If action items are still empty, expose the generated recommendations
    # as concrete next steps.
    if not normalized.get("action_items"):
        normalized["action_items"] = list(normalized.get("suggestions") or [])[:8]

    return normalized


# ============================================================
# EXPORT BUTTONS
# ============================================================

def _render_export_buttons(
    analysis: dict,
) -> None:

    st.html(
        """
        <div class="results-header">

            <div class="results-eyebrow">
                ANALYSIS COMPLETE
            </div>

            <div class="results-title">
                Resume Performance Report
            </div>

        </div>
        """
    )


    summary = _summary_text(
        analysis
    )

    st.info(summary)


    col1, col2 = st.columns(2)


    with col1:

        report_text = _build_text_report(
            analysis
        )

        st.download_button(
            "Download TXT Report",
            data=report_text,
            file_name="hiremind_resume_analysis.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_txt_report",
        )


    with col2:

        st.download_button(
            "Download JSON Report",
            data=_json_report(analysis),
            file_name="hiremind_resume_analysis.json",
            mime="application/json",
            use_container_width=True,
            key="download_json_report",
        )


# ============================================================
# REPORT HELPERS
# ============================================================

def _json_report(analysis: dict) -> str:

    import json

    return json.dumps(
        analysis,
        indent=2,
        ensure_ascii=False,
        default=str,
    )


def _build_text_report(
    analysis: dict,
) -> str:

    score = analysis.get(
        "ATS_score",
        analysis.get("ats_score", 0),
    )

    component_scores = (
        analysis.get("component_scores")
        or {}
    )

    lines = [
        "HIREMIND AI — RESUME ANALYSIS",
        "=" * 45,
        "",
        f"ATS SCORE: {float(score):.1f}/100",
        "",
        "COMPONENT SCORES",
        "-" * 25,
    ]

    for key, value in component_scores.items():

        try:
            value_text = f"{float(value):.1f}"
        except Exception:
            value_text = str(value)

        lines.append(
            f"{key.replace('_', ' ').title()}: {value_text}"
        )


    interpretation = analysis.get(
        "interpretation"
    )

    if interpretation:

        lines.extend(
            [
                "",
                "INTERPRETATION",
                "-" * 25,
                str(interpretation),
            ]
        )


    strengths = analysis.get(
        "strengths"
    ) or []

    if strengths:

        lines.extend(
            [
                "",
                "STRENGTHS",
                "-" * 25,
            ]
        )

        lines.extend(
            f"- {item}"
            for item in strengths
        )


    critical_issues = analysis.get(
        "critical_issues"
    ) or []

    if critical_issues:

        lines.extend(
            [
                "",
                "CRITICAL ISSUES",
                "-" * 25,
            ]
        )

        lines.extend(
            f"- {item}"
            for item in critical_issues
        )


    suggestions = analysis.get(
        "suggestions"
    ) or []

    if suggestions:

        lines.extend(
            [
                "",
                "SUGGESTIONS",
                "-" * 25,
            ]
        )

        lines.extend(
            f"- {item}"
            for item in suggestions
        )


    return "\n".join(lines)


# ============================================================
# MAIN PAGE
# ============================================================

def render() -> None:

    _inject_scorer_css()


    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.html(
        """
        <div class="scorer-hero">

            <div class="scorer-eyebrow">
                ✦ AI RESUME INTELLIGENCE
            </div>

            <div class="scorer-title">
                Analyze your resume.
            </div>

            <div class="scorer-title-gradient">
                Understand your opportunities.
            </div>

            <div class="scorer-description">
                Upload your resume and optionally add a job
                description to uncover ATS issues, skill gaps,
                keyword opportunities, and actionable improvements.
            </div>

        </div>
        """
    )


    # ========================================================
    # ANALYSIS MODE
    # ========================================================

    st.html(
        """
        <div class="mode-card">

            <div class="mode-label">
                Choose how you want to analyze your resume
            </div>

        </div>
        """
    )


    analysis_mode = st.radio(
        "Analysis mode",
        [
            "General ATS Score",
            "Job Description Comparison",
        ],
        horizontal=True,
        key="analysis_mode",
        label_visibility="collapsed",
    )


    # ========================================================
    # UPLOAD AREA
    # ========================================================

    resume_file, jd_file, jd_text = (
        _render_upload_area(
            analysis_mode
        )
    )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    st.html(
        "<div style='height:18px'></div>"
    )


    can_analyze = (
        resume_file is not None
    )


    if analysis_mode == "Job Description Comparison":

        can_analyze = (
            can_analyze
            and bool(
                jd_text.strip()
            )
        )


    if not can_analyze:

        if analysis_mode == "General ATS Score":

            st.info(
                "Upload your resume to start the analysis."
            )

        else:

            st.info(
                "Upload your resume and provide a job description "
                "to start the comparison."
            )


    if st.button(
        "✦  Analyze Resume",
        type="primary",
        use_container_width=True,
        disabled=not can_analyze,
        key="run_resume_analysis",
    ):

        access_token = (
            st.session_state.get(
                "access_token"
            )
        )


        if not access_token:

            st.warning(
                "Your session has expired. "
                "Please sign in again."
            )

            _navigate("login")

            return


        job_description = ""

        if analysis_mode == "Job Description Comparison":

            job_description = (
                jd_text.strip()
            )


        # ----------------------------------------------------
        # ANALYSIS
        # ----------------------------------------------------

        with st.spinner(
            "Analyzing your resume with HireMind AI..."
        ):

            try:

                analysis = (
                    api_client.analyze_resume(
                        resume_file=resume_file,
                        access_token=access_token,
                        job_description=job_description,
                    )
                )

            except Exception as exc:

                _show_backend_error(
                    exc
                )

                return


        if not analysis:

            st.error(
                "The backend returned an empty analysis."
            )

            return


        # ----------------------------------------------------
        # SAVE IN SESSION
        # ----------------------------------------------------

        analysis = _prepare_analysis_for_dashboard(analysis)

        st.session_state[
            "scorer_analysis"
        ] = analysis


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            "✓ Resume analysis completed successfully."
        )


    # ========================================================
    # PERSISTENT RESULTS
    # ========================================================
    # Render the stored analysis outside the Analyze button block.
    # Streamlit reruns the script when interactive widgets are used;
    # keeping the result here prevents the report and download buttons
    # from disappearing on rerun.

    saved_analysis = st.session_state.get("scorer_analysis")

    if saved_analysis:
        st.html("<div style='height:24px'></div>")

        display_results_dashboard(
            saved_analysis
        )

        _render_export_buttons(
            saved_analysis
        )

