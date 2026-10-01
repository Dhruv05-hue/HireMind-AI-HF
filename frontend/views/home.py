import html

import streamlit as st


# ============================================================
# NAVIGATION
# ============================================================

def _navigate(view: str) -> None:
    st.session_state["current_view"] = view
    st.rerun()


# ============================================================
# DISPLAY NAME
# ============================================================

def _get_display_name() -> str:
    """
    Get the authenticated user's username.

    New accounts use the username stored in Supabase
    user metadata. Older accounts fall back to the
    email-based display name.
    """

    username = (
        st.session_state.get("username") or ""
    ).strip()

    if username:
        return username

    email = (
        st.session_state.get("user_email") or ""
    ).strip()

    if not email:
        return "there"

    fallback_name = email.split("@")[0]

    fallback_name = (
        fallback_name
        .replace(".", " ")
        .replace("_", " ")
        .replace("-", " ")
    )

    return fallback_name.title()


# ============================================================
# GLOBAL / HOME CSS
# ============================================================

def _inject_home_css() -> None:

    st.html(
        """
        <style>

        /* ====================================================
           GLOBAL STREAMLIT LAYOUT
           ==================================================== */

        html,
        body {
            background: #070a13 !important;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 12% 8%,
                    rgba(99, 102, 241, 0.12),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 12%,
                    rgba(139, 92, 246, 0.11),
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
           REMOVE STREAMLIT TOP CHROME
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
           MAIN CONTENT AREA
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

            padding-top: 0.75rem !important;

            padding-bottom: 4rem !important;
        }


        /* ====================================================
        SIDEBAR
        ==================================================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #0d1120 0%,
                    #080b15 100%
                ) !important;

            border-right:
                1px solid rgba(255,255,255,0.10) !important;

            box-shadow:
                8px 0 35px rgba(0,0,0,0.25) !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }

        [data-testid="stSidebar"] section {
            background: transparent !important;
        }


        /* ====================================================
        SIDEBAR TEXT
        ==================================================== */

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            opacity: 1 !important;
        }


        /* Normal sidebar text */

        [data-testid="stSidebar"] {
            color: #d6d9e5 !important;
        }


        /* Sidebar headings */

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #ffffff !important;

            opacity: 1 !important;
        }


        /* Sidebar markdown */

        [data-testid="stSidebar"] .stMarkdown {
            color: #d6d9e5 !important;

            opacity: 1 !important;
        }

        [data-testid="stSidebar"] .stMarkdown p {
            color: #d6d9e5 !important;

            opacity: 1 !important;
        }


        /* ====================================================
        SIDEBAR BUTTONS
        ==================================================== */

        [data-testid="stSidebar"] .stButton {
            width: 100% !important;

            margin:
                4px 0 !important;
        }

        [data-testid="stSidebar"] .stButton > button {

            width: 100% !important;

            min-height:
                43px !important;

            padding:
                0.55rem 0.85rem !important;

            border-radius:
                11px !important;

            background:
                rgba(255,255,255,0.035) !important;

            color:
                #d8dced !important;

            border:
                1px solid
                rgba(255,255,255,0.10) !important;

            box-shadow:
                none !important;

            font-size:
                13px !important;

            font-weight:
                600 !important;

            opacity:
                1 !important;

            text-align:
                left !important;

            transition:
                background 0.2s ease,
                border-color 0.2s ease,
                color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        /* Button text */

        [data-testid="stSidebar"]
        .stButton > button p {

            color:
                #d8dced !important;

            opacity:
                1 !important;
        }


        /* Button hover */

        [data-testid="stSidebar"]
        .stButton > button:hover {

            background:
                rgba(99,102,241,0.14) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(129,140,248,0.40) !important;

            transform:
                translateX(2px) !important;

            box-shadow:
                0 6px 20px
                rgba(99,102,241,0.10) !important;
        }


        /* Hover button text */

        [data-testid="stSidebar"]
        .stButton > button:hover p {

            color:
                #ffffff !important;
        }


        /* ====================================================
        SIDEBAR SECTION LABELS
        ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-section-title {

            color:
                #8f98b0 !important;

            font-size:
                11px !important;

            font-weight:
                750 !important;

            letter-spacing:
                1.2px !important;

            text-transform:
                uppercase !important;

            opacity:
                1 !important;
        }


        /* ====================================================
        SIDEBAR USER INFORMATION
        ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-user-label {

            color:
                #9ba4b9 !important;

            font-size:
                11px !important;

            opacity:
                1 !important;
        }


        [data-testid="stSidebar"]
        .sidebar-user-email {

            color:
                #f0f2f8 !important;

            font-size:
                12px !important;

            font-weight:
                600 !important;

            opacity:
                1 !important;

            word-break:
                break-word !important;
        }


        /* ====================================================
        SIDEBAR DIVIDERS
        ==================================================== */

        [data-testid="stSidebar"] hr {

            border-color:
                rgba(255,255,255,0.08) !important;

            opacity:
                1 !important;
        }


        /* ====================================================
        SIDEBAR LINKS
        ==================================================== */

        [data-testid="stSidebar"] a {

            color:
                #c5cbe0 !important;

            opacity:
                1 !important;
        }

        [data-testid="stSidebar"] a:hover {

            color:
                #a78bfa !important;
        }


        /* ====================================================
        SIDEBAR PRIMARY BUTTON
        ==================================================== */

        [data-testid="stSidebar"]
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
                0 8px 24px
                rgba(99,102,241,0.20) !important;
        }


        [data-testid="stSidebar"]
        .stButton > button[kind="primary"] p {

            color:
                #ffffff !important;
        }


        [data-testid="stSidebar"]
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
                translateY(-1px) !important;

            box-shadow:
                0 10px 30px
                rgba(99,102,241,0.32) !important;
        }


        /* ====================================================
        SIDEBAR SCROLLBAR
        ==================================================== */

        [data-testid="stSidebar"] ::-webkit-scrollbar {
            width: 5px;
        }

        [data-testid="stSidebar"] ::-webkit-scrollbar-track {
            background:
                transparent;
        }

        [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
            background:
                rgba(129,140,248,0.25);

            border-radius:
                10px;
        }

        /* ====================================================
           HERO
           ==================================================== */

        .home-hero {

            position: relative;

            overflow: hidden;

            padding:
                34px 36px;

            margin-bottom:
                30px;

            border-radius:
                24px;

            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(139, 92, 246, 0.20),
                    transparent 32%
                ),
                radial-gradient(
                    circle at 8% 90%,
                    rgba(99, 102, 241, 0.14),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    rgba(22, 27, 52, 0.96),
                    rgba(12, 16, 31, 0.96)
                );

            border:
                1px solid
                rgba(255, 255, 255, 0.075);

            box-shadow:
                0 24px 65px
                rgba(0, 0, 0, 0.30),

                inset 0 1px 0
                rgba(255, 255, 255, 0.04);
        }


        .home-hero::after {

            content: "";

            position: absolute;

            width: 260px;
            height: 260px;

            right: -100px;
            top: -130px;

            border-radius: 50%;

            background:
                rgba(129, 140, 248, 0.08);

            filter: blur(20px);

            pointer-events: none;
        }


        .home-eyebrow {

            position: relative;

            z-index: 1;

            color: #818cf8;

            font-size: 10px;

            font-weight: 800;

            letter-spacing:
                1.6px;

            text-transform:
                uppercase;

            margin-bottom:
                11px;
        }


        .home-title {

            position: relative;

            z-index: 1;

            color: #ffffff;

            font-size: 34px;

            font-weight: 800;

            line-height: 1.15;

            letter-spacing:
                -1.2px;

            margin-bottom:
                11px;
        }


        .home-title span {

            background:
                linear-gradient(
                    90deg,
                    #818cf8,
                    #c084fc
                );

            -webkit-background-clip:
                text;

            -webkit-text-fill-color:
                transparent;
        }


        .home-description {

            position: relative;

            z-index: 1;

            max-width: 760px;

            color: #929bb0;

            font-size: 13px;

            line-height: 1.7;
        }


        /* ====================================================
           SECTION HEADERS
           ==================================================== */

        .section-label {

            color: #ffffff;

            font-size: 19px;

            font-weight: 750;

            letter-spacing:
                -0.3px;

            margin:
                28px 0 7px 2px;
        }


        .section-description {

            color: #777f94;

            font-size: 12px;

            line-height: 1.5;

            margin:
                0 0 17px 2px;
        }


        /* ====================================================
           ACTION CARDS
           ==================================================== */

        .action-card {

            min-height: 205px;

            padding:
                23px;

            border-radius:
                19px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20, 25, 45, 0.84),
                    rgba(11, 15, 28, 0.84)
                );

            border:
                1px solid
                rgba(255, 255, 255, 0.07);

            box-shadow:
                0 12px 35px
                rgba(0, 0, 0, 0.18),

                inset 0 1px 0
                rgba(255, 255, 255, 0.025);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }


        .action-card:hover {

            transform:
                translateY(-3px);

            border-color:
                rgba(129, 140, 248, 0.18);

            box-shadow:
                0 18px 45px
                rgba(0, 0, 0, 0.24);
        }


        .action-icon {

            width: 43px;
            height: 43px;

            display: flex;

            align-items: center;
            justify-content: center;

            border-radius:
                13px;

            margin-bottom:
                17px;

            background:
                rgba(99, 102, 241, 0.12);

            border:
                1px solid
                rgba(129, 140, 248, 0.14);

            font-size:
                20px;
        }


        .action-title {

            color: #ffffff;

            font-size:
                16px;

            font-weight:
                700;

            margin-bottom:
                7px;
        }


        .action-description {

            color: #7f889d;

            font-size:
                12px;

            line-height:
                1.55;
        }


        /* ====================================================
           WORKFLOW
           ==================================================== */

        .workflow-card {

            min-height:
                155px;

            padding:
                22px;

            border-radius:
                18px;

            background:
                rgba(17, 21, 38, 0.68);

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }


        .workflow-card:hover {

            transform:
                translateY(-2px);

            border-color:
                rgba(129, 140, 248, 0.16);
        }


        .workflow-number {

            color:
                #818cf8;

            font-size:
                10px;

            font-weight:
                800;

            letter-spacing:
                1.3px;

            margin-bottom:
                12px;
        }


        .workflow-title {

            color:
                #ffffff;

            font-size:
                15px;

            font-weight:
                700;

            margin-bottom:
                6px;
        }


        .workflow-text {

            color:
                #7c8599;

            font-size:
                12px;

            line-height:
                1.55;
        }


        /* ====================================================
           FEATURE CARDS
           ==================================================== */

        .feature-card {

            min-height:
                145px;

            padding:
                20px;

            border-radius:
                17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20, 25, 45, 0.72),
                    rgba(13, 17, 30, 0.72)
                );

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease;
        }


        .feature-card:hover {

            transform:
                translateY(-2px);

            border-color:
                rgba(129, 140, 248, 0.16);
        }


        .feature-icon {

            font-size:
                22px;

            margin-bottom:
                10px;
        }


        .feature-title {

            color:
                #ffffff;

            font-size:
                14px;

            font-weight:
                700;

            margin-bottom:
                5px;
        }


        .feature-text {

            color:
                #788196;

            font-size:
                11px;

            line-height:
                1.5;
        }


        /* ====================================================
           CTA
           ==================================================== */

        .home-cta {

            margin-top:
                30px;

            padding:
                28px;

            border-radius:
                20px;

            text-align:
                center;

            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(129, 140, 248, 0.13),
                    transparent 55%
                ),
                rgba(17, 21, 38, 0.72);

            border:
                1px solid
                rgba(129, 140, 248, 0.11);
        }


        .cta-title {

            color:
                #ffffff;

            font-size:
                19px;

            font-weight:
                750;

            margin-bottom:
                7px;
        }


        .cta-text {

            color:
                #7f889d;

            font-size:
                12px;
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
                box-shadow 0.2s ease,
                border-color 0.2s ease,
                background 0.2s ease !important;
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
                rgba(129, 140, 248, 0.55) !important;

            box-shadow:
                0 8px 25px
                rgba(99, 102, 241, 0.20) !important;
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
                rgba(99, 102, 241, 0.32) !important;
        }


        .stButton > button:not([kind="primary"]) {

            background:
                rgba(255, 255, 255, 0.035) !important;

            color:
                #c7cbe0 !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.10) !important;
        }


        .stButton > button:not([kind="primary"]):hover {

            background:
                rgba(129, 140, 248, 0.09) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(129, 140, 248, 0.35) !important;

            transform:
                translateY(-2px) !important;

            box-shadow:
                0 8px 25px
                rgba(99, 102, 241, 0.10) !important;
        }


        /* ====================================================
           MOBILE
           ==================================================== */

        @media (max-width: 900px) {

            .home-title {
                font-size:
                    29px;
            }

            .home-hero {
                padding:
                    28px 24px;
            }
        }


        @media (max-width: 700px) {

            .block-container {
                padding-left:
                    1rem !important;

                padding-right:
                    1rem !important;
            }

            .home-title {
                font-size:
                    26px;
            }

            .home-hero {
                padding:
                    24px 20px;
            }

            .action-card {
                min-height:
                    auto;
            }
        }

        </style>
        """
    )


# ============================================================
# MAIN DASHBOARD
# ============================================================

def render() -> None:

    _inject_home_css()

    display_name = html.escape(
        _get_display_name()
    )


    # ========================================================
    # HERO
    # ========================================================

    st.html(
        f"""
        <div class="home-hero">

            <div class="home-eyebrow">
                HIREMIND AI · PERSONAL DASHBOARD
            </div>

            <div class="home-title">
                Welcome back,
                <span>{display_name}</span> 👋
            </div>

            <div class="home-description">
                Turn your resume into a stronger job application.
                Analyze ATS compatibility, compare your resume with
                job descriptions, discover missing skills, and get
                actionable AI-powered recommendations.
            </div>

        </div>
        """
    )


    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    st.html(
        """
        <div class="section-label">
            What would you like to do?
        </div>

        <div class="section-description">
            Choose a tool to get started.
        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    # ========================================================
    # ANALYZE RESUME
    # ========================================================

    with col1:

        st.html(
            """
            <div class="action-card">

                <div class="action-icon">
                    📄
                </div>

                <div class="action-title">
                    Analyze Resume
                </div>

                <div class="action-description">
                    Get a complete ATS score, content analysis,
                    keyword evaluation, skill validation, and
                    improvement recommendations.
                </div>

            </div>
            """
        )

        st.html(
            "<div style='height:10px'></div>"
        )

        if st.button(
            "Analyze Resume →",
            type="primary",
            use_container_width=True,
            key="home_analyze",
        ):
            _navigate("scorer")


    # ========================================================
    # ANALYSIS HISTORY
    # ========================================================

    with col2:

        st.html(
            """
            <div class="action-card">

                <div class="action-icon">
                    📊
                </div>

                <div class="action-title">
                    Analysis History
                </div>

                <div class="action-description">
                    Review previous resume analyses and keep
                    track of your ATS performance over time.
                </div>

            </div>
            """
        )

        st.html(
            "<div style='height:10px'></div>"
        )

        if st.button(
            "View History →",
            use_container_width=True,
            key="home_history",
        ):
            _navigate("history")


    # ========================================================
    # RESOURCES
    # ========================================================

    with col3:

        st.html(
            """
            <div class="action-card">

                <div class="action-icon">
                    📚
                </div>

                <div class="action-title">
                    Career Resources
                </div>

                <div class="action-description">
                    Explore resume and career resources to help
                    you prepare for your next opportunity.
                </div>

            </div>
            """
        )

        st.html(
            "<div style='height:10px'></div>"
        )

        if st.button(
            "Explore Resources →",
            use_container_width=True,
            key="home_resources",
        ):
            _navigate("resources")


    # ========================================================
    # HOW IT WORKS
    # ========================================================

    st.html(
        """
        <div class="section-label">
            How HireMind AI works
        </div>

        <div class="section-description">
            Three simple steps to improve your resume.
        </div>
        """
    )


    step1, step2, step3 = st.columns(3)


    with step1:

        st.html(
            """
            <div class="workflow-card">

                <div class="workflow-number">
                    STEP 01
                </div>

                <div class="workflow-title">
                    Upload
                </div>

                <div class="workflow-text">
                    Upload your PDF, DOC, or DOCX resume and,
                    optionally, provide a target job description.
                </div>

            </div>
            """
        )


    with step2:

        st.html(
            """
            <div class="workflow-card">

                <div class="workflow-number">
                    STEP 02
                </div>

                <div class="workflow-title">
                    Analyze
                </div>

                <div class="workflow-text">
                    HireMind AI evaluates your resume using NLP,
                    semantic matching, skill validation, and
                    ATS-focused scoring.
                </div>

            </div>
            """
        )


    with step3:

        st.html(
            """
            <div class="workflow-card">

                <div class="workflow-number">
                    STEP 03
                </div>

                <div class="workflow-title">
                    Improve
                </div>

                <div class="workflow-text">
                    Understand your strengths, identify gaps,
                    and follow targeted recommendations to
                    improve your application.
                </div>

            </div>
            """
        )


    # ========================================================
    # FEATURES
    # ========================================================

    st.html(
        """
        <div class="section-label">
            Your AI resume toolkit
        </div>

        <div class="section-description">
            Everything you need to understand and improve your resume.
        </div>
        """
    )


    feature1, feature2, feature3 = st.columns(3)


    with feature1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🎯
                </div>

                <div class="feature-title">
                    ATS Score
                </div>

                <div class="feature-text">
                    Understand how your resume performs across
                    important ATS-related dimensions.
                </div>

            </div>
            """
        )


    with feature2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🔎
                </div>

                <div class="feature-title">
                    JD Matching
                </div>

                <div class="feature-text">
                    Compare your resume with a target job
                    description using keyword and semantic signals.
                </div>

            </div>
            """
        )


    with feature3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🧠
                </div>

                <div class="feature-title">
                    Skill Validation
                </div>

                <div class="feature-text">
                    Identify which skills in your resume have
                    supporting evidence from your experience and projects.
                </div>

            </div>
            """
        )


    feature4, feature5, feature6 = st.columns(3)


    with feature4:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💡
                </div>

                <div class="feature-title">
                    Smart Recommendations
                </div>

                <div class="feature-text">
                    Receive practical suggestions for improving
                    your resume.
                </div>

            </div>
            """
        )


    with feature5:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📈
                </div>

                <div class="feature-title">
                    Track Progress
                </div>

                <div class="feature-text">
                    Keep previous analyses available so you can
                    compare future improvements.
                </div>

            </div>
            """
        )


    with feature6:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ⚡
                </div>

                <div class="feature-title">
                    Fast Feedback
                </div>

                <div class="feature-text">
                    Go from uploaded resume to actionable insights
                    without manually reviewing every section.
                </div>

            </div>
            """
        )


    # ========================================================
    # FINAL CTA
    # ========================================================

    st.html(
        """
        <div class="home-cta">

            <div class="cta-title">
                Ready to see how your resume performs?
            </div>

            <div class="cta-text">
                Upload your resume and start your first AI analysis.
            </div>

        </div>
        """
    )

    st.html(
        "<div style='height:12px'></div>"
    )


    if st.button(
        "🚀 Start Resume Analysis",
        type="primary",
        use_container_width=True,
        key="home_bottom_analyze",
    ):
        _navigate("scorer")