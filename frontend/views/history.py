import requests
import streamlit as st

from frontend.services import api_client


# ============================================================
# BACKEND ERROR
# ============================================================

def _show_backend_error(exc: Exception) -> None:

    if isinstance(exc, requests.ConnectionError):

        st.error(
            "Could not reach the backend. Is it running on port 8000?"
        )

    elif isinstance(exc, requests.HTTPError) and exc.response is not None:

        st.error(
            f"Backend returned {exc.response.status_code}: "
            f"{exc.response.text}"
        )

    else:

        st.error(
            f"Unexpected error: {exc}"
        )


# ============================================================
# CSS
# ============================================================

def _inject_history_css() -> None:

    st.html(
        """
        <style>

        /* ====================================================
           GLOBAL
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

            max-width:
                1250px !important;

            padding-top:
                0.8rem !important;

            padding-bottom:
                4rem !important;
        }


        /* ====================================================
           REMOVE STREAMLIT HEADER
           ==================================================== */

        [data-testid="stHeader"] {

            height:
                0 !important;

            min-height:
                0 !important;

            background:
                transparent !important;

            border:
                none !important;
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
           SIDEBAR
           SAME AS ANALYZE RESUME
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

            box-shadow:
                8px 0 35px
                rgba(0,0,0,0.22) !important;
        }

        [data-testid="stSidebar"] > div:first-child {

            background:
                transparent !important;
        }


        /* Force sidebar elements to remain visible */

        [data-testid="stSidebar"] * {

            opacity:
                1 !important;
        }


        /* Sidebar text */

        [data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"]
        p {

            color:
                #cbd1e1 !important;

            opacity:
                1 !important;
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

            font-size:
                11px !important;

            font-weight:
                800 !important;

            letter-spacing:
                1.2px !important;

            text-transform:
                uppercase !important;
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


        /* Sidebar account */

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


        /* Sidebar navigation */

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


        /* ====================================================
           HISTORY HERO
           ==================================================== */

        .history-hero {

            position:
                relative;

            overflow:
                hidden;

            padding:
                30px 34px;

            margin-bottom:
                24px;

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


        .history-eyebrow {

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


        .history-title {

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
                0 0 8px 0;
        }


        .history-description {

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
           SUMMARY CARD
           ==================================================== */

        .history-summary {

            display:
                flex;

            align-items:
                center;

            justify-content:
                space-between;

            padding:
                18px 21px;

            margin-bottom:
                25px;

            border-radius:
                16px;

            background:
                rgba(17,21,38,0.70);

            border:
                1px solid
                rgba(255,255,255,0.07);
        }


        .summary-label {

            color:
                #8d96aa;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.2px;

            text-transform:
                uppercase;
        }


        .summary-value {

            color:
                #ffffff;

            font-size:
                25px;

            font-weight:
                800;

            margin-top:
                2px;
        }


        .summary-icon {

            width:
                46px;

            height:
                46px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                13px;

            background:
                rgba(99,102,241,0.12);

            border:
                1px solid
                rgba(129,140,248,0.20);

            font-size:
                20px;
        }


        /* ====================================================
           SECTION TITLE
           ==================================================== */

        .history-section-title {

            color:
                #ffffff;

            font-size:
                19px;

            font-weight:
                750;

            margin:
                0 0 5px 0;
        }


        .history-section-description {

            color:
                #7f889d;

            font-size:
                12px;

            margin-bottom:
                17px;
        }


        /* ====================================================
           EXPANDERS
           ==================================================== */

        [data-testid="stExpander"] {

            background:
                linear-gradient(
                    145deg,
                    rgba(20,25,45,0.90),
                    rgba(11,15,28,0.90)
                ) !important;

            border:
                1px solid
                rgba(255,255,255,0.08) !important;

            border-radius:
                17px !important;

            margin-bottom:
                13px !important;

            overflow:
                hidden !important;

            box-shadow:
                0 10px 30px
                rgba(0,0,0,0.15) !important;
        }


        [data-testid="stExpander"]:hover {

            border-color:
                rgba(129,140,248,0.28) !important;

            box-shadow:
                0 14px 40px
                rgba(0,0,0,0.22) !important;
        }


        [data-testid="stExpander"]
        summary {

            background:
                transparent !important;

            padding:
                17px 20px !important;
        }


        [data-testid="stExpander"]
        summary:hover {

            background:
                rgba(99,102,241,0.055) !important;
        }


        [data-testid="stExpander"]
        summary p {

            color:
                #eef0f7 !important;

            font-size:
                13px !important;

            font-weight:
                700 !important;
        }


        /* ====================================================
           METRICS
           ==================================================== */

        [data-testid="stMetric"] {

            background:
                rgba(255,255,255,0.035) !important;

            border:
                1px solid
                rgba(255,255,255,0.07) !important;

            border-radius:
                13px !important;

            padding:
                15px 16px !important;
        }


        [data-testid="stMetricLabel"] {

            color:
                #858ea3 !important;
        }


        [data-testid="stMetricValue"] {

            color:
                #ffffff !important;

            font-weight:
                800 !important;
        }


        /* ====================================================
           JD MATCH
           ==================================================== */

        .jd-match-card {

            margin-top:
                18px;

            margin-bottom:
                18px;

            padding:
                17px 19px;

            border-radius:
                14px;

            background:

                linear-gradient(
                    135deg,
                    rgba(99,102,241,0.10),
                    rgba(139,92,246,0.07)
                );

            border:
                1px solid
                rgba(129,140,248,0.15);
        }


        .jd-match-label {

            color:
                #858da4;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1px;

            text-transform:
                uppercase;

            margin-bottom:
                4px;
        }


        .jd-match-value {

            color:
                #a78bfa;

            font-size:
                25px;

            font-weight:
                800;
        }


        /* ====================================================
           BUTTONS
           ==================================================== */

        .stButton > button {

            min-height:
                43px !important;

            border-radius:
                11px !important;

            font-weight:
                650 !important;

            transition:
                all 0.2s ease !important;
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
                rgba(129,140,248,0.10) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(129,140,248,0.35) !important;

            transform:
                translateY(-1px) !important;
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
                rgba(99,102,241,0.30) !important;
        }


        /* ====================================================
           EMPTY STATE
           ==================================================== */

        .history-empty {

            text-align:
                center;

            padding:
                55px 30px;

            margin-top:
                20px;

            border-radius:
                20px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20,25,45,0.90),
                    rgba(11,15,28,0.90)
                );

            border:
                1px solid
                rgba(255,255,255,0.08);
        }


        .history-empty-icon {

            width:
                62px;

            height:
                62px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            margin:
                0 auto 15px auto;

            border-radius:
                18px;

            background:
                rgba(99,102,241,0.12);

            border:
                1px solid
                rgba(129,140,248,0.18);

            font-size:
                27px;
        }


        .history-empty-title {

            color:
                #ffffff;

            font-size:
                21px;

            font-weight:
                750;

            margin-bottom:
                7px;
        }


        .history-empty-text {

            color:
                #7f889d;

            font-size:
                13px;

            line-height:
                1.6;

            max-width:
                520px;

            margin:
                0 auto 22px auto;
        }


        /* ====================================================
           ALERTS
           ==================================================== */

        [data-testid="stAlert"] {

            border-radius:
                12px !important;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 700px) {

            .history-title {
                font-size:
                    27px;
            }

            .history-hero {
                padding:
                    26px 22px;
            }

            .history-summary {
                padding:
                    16px;
            }
        }

        </style>
        """
    )


# ============================================================
# MAIN PAGE
# ============================================================

def render() -> None:

    _inject_history_css()

    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="history-hero">

            <div class="history-eyebrow">
                HIREMIND AI · RESUME INTELLIGENCE
            </div>

            <div class="history-title">
                Analysis History
            </div>

            <div class="history-description">
                Review your previous resume analyses, track your
                ATS performance, and see how your applications
                improve over time.
            </div>

        </div>
        """
    )


    # ========================================================
    # AUTHENTICATION
    # ========================================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.html(
            """
            <div class="history-empty">

                <div class="history-empty-icon">
                    🔐
                </div>

                <div class="history-empty-title">
                    Sign in to view your history
                </div>

                <div class="history-empty-text">
                    Your previous resume analyses are securely
                    linked to your account. Sign in to access
                    your reports.
                </div>

            </div>
            """
        )

        if st.button(
            "Sign in →",
            type="primary",
        ):

            st.session_state.current_view = "login"

            st.rerun()

        return


    # ========================================================
    # LOAD HISTORY
    # ========================================================

    try:

        history = api_client.get_history(
            access_token
        )

    except requests.RequestException as exc:

        _show_backend_error(exc)

        return


    # ========================================================
    # EMPTY HISTORY
    # ========================================================

    if not history:

        st.html(
            """
            <div class="history-empty">

                <div class="history-empty-icon">
                    📊
                </div>

                <div class="history-empty-title">
                    No analyses yet
                </div>

                <div class="history-empty-text">
                    Once you analyze a resume, your ATS reports
                    will appear here so you can track your
                    progress over time.
                </div>

            </div>
            """
        )

        if st.button(
            "🎯 Analyze Your Resume",
            type="primary",
        ):

            st.session_state.current_view = "scorer"

            st.rerun()

        return


    # ========================================================
    # SUMMARY
    # ========================================================

    st.html(
        f"""
        <div class="history-summary">

            <div>

                <div class="summary-label">
                    Total analyses
                </div>

                <div class="summary-value">
                    {len(history)}
                </div>

            </div>

            <div class="summary-icon">
                📊
            </div>

        </div>
        """
    )


    # ========================================================
    # SECTION HEADER
    # ========================================================

    st.html(
        """
        <div class="history-section-title">
            Your previous analyses
        </div>

        <div class="history-section-description">
            Expand an analysis to view its ATS score and
            detailed performance breakdown.
        </div>
        """
    )


    # ========================================================
    # HISTORY
    # ========================================================

    for idx, entry in enumerate(history):

        filename = entry.get(
            "filename",
            "resume",
        )

        try:

            ats_score = float(
                entry.get(
                    "ats_score",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            ats_score = 0.0


        created_at = entry.get(
            "created_at",
            "",
        )


        analysis = (
            entry.get(
                "analysis_result",
                {},
            )
            or {}
        )


        component_scores = (
            analysis.get(
                "component_scores",
                {},
            )
            or {}
        )


        jd_comparison = (
            analysis.get(
                "jd_comparison"
            )
            or analysis.get(
                "jd_match_analysis"
            )
        )


        # ====================================================
        # ANALYSIS CARD
        # ====================================================

        with st.expander(
            (
                f"📄  {filename}   •   "
                f"Score: {ats_score:.0f}/100   •   "
                f"{created_at}"
            ),
            expanded=False,
        ):

            # ------------------------------------------------
            # SCORE GRID
            # ------------------------------------------------

            c1, c2, c3 = st.columns(3)


            with c1:

                st.metric(
                    "Overall",
                    f"{ats_score:.0f}/100",
                )

                st.metric(
                    "Formatting",
                    (
                        f"{component_scores.get('formatting', 0):.0f}"
                        "/20"
                    ),
                )


            with c2:

                st.metric(
                    "Keywords",
                    (
                        f"{component_scores.get('keywords', 0):.0f}"
                        "/25"
                    ),
                )

                st.metric(
                    "Content",
                    (
                        f"{component_scores.get('content', 0):.0f}"
                        "/25"
                    ),
                )


            with c3:

                st.metric(
                    "Skill Validation",
                    (
                        f"{component_scores.get('skill_validation', 0):.0f}"
                        "/15"
                    ),
                )

                st.metric(
                    "ATS Compatibility",
                    (
                        f"{component_scores.get('ats_compatibility', 0):.0f}"
                        "/15"
                    ),
                )


            # ------------------------------------------------
            # JD MATCH
            # ------------------------------------------------

            if jd_comparison:

                try:

                    jd_match = float(
                        jd_comparison.get(
                            "match_percentage",
                            0,
                        )
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    jd_match = 0.0


                st.html(
                    f"""
                    <div class="jd-match-card">

                        <div class="jd-match-label">
                            Job Description Match
                        </div>

                        <div class="jd-match-value">
                            {jd_match:.0f}%
                        </div>

                    </div>
                    """
                )


            # ------------------------------------------------
            # DELETE
            # ------------------------------------------------

            entry_id = entry.get(
                "id"
            )


            if entry_id:

                if st.button(
                    "🗑️ Delete Analysis",
                    key=f"delete_{idx}",
                ):

                    try:

                        api_client.delete_history_entry(
                            str(entry_id),
                            access_token,
                        )

                        st.success(
                            "Analysis deleted successfully."
                        )

                        st.rerun()

                    except requests.RequestException as exc:

                        _show_backend_error(
                            exc
                        )