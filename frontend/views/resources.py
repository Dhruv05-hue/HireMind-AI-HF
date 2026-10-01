import streamlit as st


# ============================================================
# RESOURCES PAGE CSS
# ============================================================

def _inject_resources_css() -> None:

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
                    circle at 8% 5%,
                    rgba(99,102,241,0.11),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 92% 8%,
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
           SAME STYLE AS ANALYZE RESUME
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


        [data-testid="stSidebar"] * {

            opacity:
                1 !important;
        }


        [data-testid="stSidebar"]
        [data-testid="stMarkdownContainer"]
        p {

            color:
                #cbd1e1 !important;

            opacity:
                1 !important;
        }


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
           HERO
           ==================================================== */

        .resources-hero {

            position:
                relative;

            overflow:
                hidden;

            padding:
                32px 35px;

            margin-bottom:
                25px;

            border-radius:
                22px;

            background:

                radial-gradient(
                    circle at 88% 12%,
                    rgba(139,92,246,0.20),
                    transparent 32%
                ),

                radial-gradient(
                    circle at 8% 90%,
                    rgba(99,102,241,0.13),
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


        .resources-eyebrow {

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
                9px;
        }


        .resources-title {

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

            margin-bottom:
                8px;
        }


        .resources-title-gradient {

            background:
                linear-gradient(
                    90deg,
                    #a78bfa,
                    #818cf8
                );

            -webkit-background-clip:
                text;

            -webkit-text-fill-color:
                transparent;
        }


        .resources-description {

            color:
                #a5aec2;

            font-size:
                13px;

            line-height:
                1.7;

            max-width:
                720px;
        }


        /* ====================================================
           SECTION HEADER
           ==================================================== */

        .resources-section {

            margin-top:
                28px;

            margin-bottom:
                15px;
        }


        .resources-section-title {

            color:
                #ffffff;

            font-size:
                22px;

            font-weight:
                750;

            letter-spacing:
                -0.4px;
        }


        .resources-section-description {

            color:
                #7f889d;

            font-size:
                12px;

            margin-top:
                5px;
        }


        /* ====================================================
           DO / DON'T CARDS
           ==================================================== */

        .tips-grid {

            display:
                grid;

            grid-template-columns:
                1fr 1fr;

            gap:
                17px;

            margin-top:
                16px;
        }


        .tips-card {

            padding:
                23px 24px;

            border-radius:
                17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20,25,45,0.92),
                    rgba(11,15,28,0.92)
                );

            border:
                1px solid
                rgba(255,255,255,0.075);

            box-shadow:
                0 12px 35px
                rgba(0,0,0,0.16);
        }


        .tips-card:hover {

            border-color:
                rgba(129,140,248,0.25);

            transform:
                translateY(-1px);
        }


        .tips-card-header {

            display:
                flex;

            align-items:
                center;

            gap:
                10px;

            color:
                #ffffff;

            font-size:
                17px;

            font-weight:
                750;

            margin-bottom:
                17px;
        }


        .tips-icon {

            width:
                34px;

            height:
                34px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                10px;

            font-size:
                17px;
        }


        .do-icon {

            background:
                rgba(34,197,94,0.12);

            border:
                1px solid
                rgba(34,197,94,0.20);
        }


        .dont-icon {

            background:
                rgba(244,63,94,0.12);

            border:
                1px solid
                rgba(244,63,94,0.20);
        }


        .tips-list {

            margin:
                0;

            padding:
                0;

            list-style:
                none;
        }


        .tips-list li {

            position:
                relative;

            color:
                #aeb6c9;

            font-size:
                12px;

            line-height:
                1.55;

            padding:
                7px 0 7px 20px;

            border-bottom:
                1px solid
                rgba(255,255,255,0.045);
        }


        .tips-list li:last-child {

            border-bottom:
                none;
        }


        .do-card .tips-list li::before {

            content:
                "✓";

            position:
                absolute;

            left:
                0;

            color:
                #4ade80;

            font-weight:
                800;
        }


        .dont-card .tips-list li::before {

            content:
                "×";

            position:
                absolute;

            left:
                1px;

            color:
                #fb7185;

            font-size:
                16px;

            font-weight:
                700;
        }


        /* ====================================================
           DIVIDER
           ==================================================== */

        .resources-divider {

            height:
                1px;

            margin:
                30px 0;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(255,255,255,0.10),
                    transparent
                );
        }


        /* ====================================================
           INDUSTRY SECTION
           ==================================================== */

        .industry-card {

            padding:
                24px;

            border-radius:
                17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20,25,45,0.92),
                    rgba(11,15,28,0.92)
                );

            border:
                1px solid
                rgba(255,255,255,0.075);

            margin-top:
                13px;
        }


        .industry-title {

            color:
                #ffffff;

            font-size:
                17px;

            font-weight:
                750;

            margin-bottom:
                15px;
        }


        .keyword-grid {

            display:
                grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap:
                10px;
        }


        .keyword-item {

            padding:
                12px 14px;

            border-radius:
                10px;

            background:
                rgba(255,255,255,0.035);

            border:
                1px solid
                rgba(255,255,255,0.06);

            color:
                #aeb6c9;

            font-size:
                12px;

            line-height:
                1.45;
        }


        .keyword-item strong {

            color:
                #e5e7ef;

            font-weight:
                650;
        }


        /* ====================================================
           TABS
           ==================================================== */

        [data-testid="stTabs"] {

            margin-top:
                15px;
        }


        [data-testid="stTabs"] [role="tablist"] {

            gap:
                8px;

            border-bottom:
                1px solid
                rgba(255,255,255,0.07);
        }


        [data-testid="stTabs"] button {

            color:
                #858ea3 !important;

            font-size:
                12px !important;

            font-weight:
                650 !important;

            background:
                transparent !important;

            border-radius:
                8px 8px 0 0 !important;
        }


        [data-testid="stTabs"] button:hover {

            color:
                #ffffff !important;
        }


        [data-testid="stTabs"] button[aria-selected="true"] {

            color:
                #a78bfa !important;
        }


        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {

            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #a855f7
                ) !important;
        }


        /* ====================================================
           TEMPLATE CARD
           ==================================================== */

        .template-card {

            display:
                flex;

            align-items:
                center;

            gap:
                18px;

            padding:
                22px;

            margin-top:
                20px;

            border-radius:
                16px;

            background:
                linear-gradient(
                    135deg,
                    rgba(99,102,241,0.10),
                    rgba(139,92,246,0.06)
                );

            border:
                1px solid
                rgba(129,140,248,0.16);
        }


        .template-icon {

            width:
                50px;

            height:
                50px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            flex-shrink:
                0;

            border-radius:
                13px;

            background:
                rgba(99,102,241,0.13);

            border:
                1px solid
                rgba(129,140,248,0.20);

            font-size:
                22px;
        }


        .template-title {

            color:
                #ffffff;

            font-size:
                15px;

            font-weight:
                700;

            margin-bottom:
                4px;
        }


        .template-description {

            color:
                #8992a8;

            font-size:
                12px;

            line-height:
                1.5;
        }


        /* ====================================================
           MOBILE
           ==================================================== */

        @media (max-width: 750px) {

            .resources-title {
                font-size:
                    28px;
            }

            .resources-hero {
                padding:
                    26px 22px;
            }

            .tips-grid {
                grid-template-columns:
                    1fr;
            }

            .keyword-grid {
                grid-template-columns:
                    1fr;
            }

        }

        </style>
        """
    )


# ============================================================
# PAGE
# ============================================================

def render():

    _inject_resources_css()


    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="resources-hero">

            <div class="resources-eyebrow">
                HIREMIND AI · CAREER INTELLIGENCE
            </div>

            <div class="resources-title">
                Resources
                <span class="resources-title-gradient">
                    & Tips
                </span>
            </div>

            <div class="resources-description">
                Practical guidance to build cleaner, stronger,
                and more ATS-friendly resumes that are easier
                for recruiters and applicant tracking systems
                to understand.
            </div>

        </div>
        """
    )


    # ========================================================
    # ATS OPTIMIZATION
    # ========================================================

    st.html(
        """
        <div class="resources-section">

            <div class="resources-section-title">
                🎯 ATS Optimization Tips
            </div>

            <div class="resources-section-description">
                Follow these practical guidelines when preparing
                your resume for automated screening systems.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="tips-grid">

            <div class="tips-card do-card">

                <div class="tips-card-header">

                    <div class="tips-icon do-icon">
                        ✓
                    </div>

                    Do's

                </div>

                <ul class="tips-list">

                    <li>
                        Use standard section headings
                    </li>

                    <li>
                        Include relevant keywords from job description
                    </li>

                    <li>
                        Use simple, clean formatting
                    </li>

                    <li>
                        List skills explicitly
                    </li>

                    <li>
                        Quantify achievements with numbers
                    </li>

                    <li>
                        Use standard fonts
                        (Arial, Calibri, Times New Roman)
                    </li>

                    <li>
                        Save as PDF or DOCX
                    </li>

                </ul>

            </div>


            <div class="tips-card dont-card">

                <div class="tips-card-header">

                    <div class="tips-icon dont-icon">
                        ×
                    </div>

                    Don'ts

                </div>

                <ul class="tips-list">

                    <li>
                        Avoid tables and text boxes
                    </li>

                    <li>
                        Don't use headers/footers for important info
                    </li>

                    <li>
                        Avoid images and graphics
                    </li>

                    <li>
                        Don't use unusual fonts
                    </li>

                    <li>
                        Avoid columns
                        (use single column layout)
                    </li>

                    <li>
                        Don't keyword stuff
                    </li>

                    <li>
                        Avoid abbreviations without spelling out first
                    </li>

                </ul>

            </div>

        </div>
        """
    )


    # ========================================================
    # DIVIDER
    # ========================================================

    st.html(
        """
        <div class="resources-divider"></div>
        """
    )


    # ========================================================
    # COMMON KEYWORDS
    # ========================================================

    st.html(
        """
        <div class="resources-section">

            <div class="resources-section-title">
                🔑 Common ATS Keywords by Industry
            </div>

            <div class="resources-section-description">
                Explore common terminology that can appear in
                resumes across different career fields.
            </div>

        </div>
        """
    )


    # ========================================================
    # INDUSTRY TABS
    # ========================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "💻 Tech",
            "💼 Business",
            "🎨 Creative",
        ]
    )


    # ========================================================
    # TECH
    # ========================================================

    with tab1:

        st.html(
            """
            <div class="industry-card">

                <div class="industry-title">
                    Software Development
                </div>

                <div class="keyword-grid">

                    <div class="keyword-item">
                        <strong>Programming Languages</strong><br>
                        Python, Java, JavaScript
                    </div>

                    <div class="keyword-item">
                        <strong>Frameworks</strong><br>
                        React, Django, Spring
                    </div>

                    <div class="keyword-item">
                        <strong>Tools</strong><br>
                        Git, Docker, Kubernetes
                    </div>

                    <div class="keyword-item">
                        <strong>Methodologies</strong><br>
                        Agile, Scrum, CI/CD
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # BUSINESS
    # ========================================================

    with tab2:

        st.html(
            """
            <div class="industry-card">

                <div class="industry-title">
                    Business & Management
                </div>

                <div class="keyword-grid">

                    <div class="keyword-item">
                        <strong>Project Management</strong><br>
                        Planning, execution, delivery
                    </div>

                    <div class="keyword-item">
                        <strong>Stakeholder Engagement</strong><br>
                        Communication, collaboration
                    </div>

                    <div class="keyword-item">
                        <strong>Budget Management</strong><br>
                        Budgeting, forecasting, reporting
                    </div>

                    <div class="keyword-item">
                        <strong>Strategic Planning</strong><br>
                        Strategy, analysis, business planning
                    </div>

                    <div class="keyword-item">
                        <strong>Team Leadership</strong><br>
                        Leadership, mentoring, team development
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # CREATIVE
    # ========================================================

    with tab3:

        st.html(
            """
            <div class="industry-card">

                <div class="industry-title">
                    Creative & Design
                </div>

                <div class="keyword-grid">

                    <div class="keyword-item">
                        <strong>Design Tools</strong><br>
                        Adobe Creative Suite
                    </div>

                    <div class="keyword-item">
                        <strong>UI / UX Design</strong><br>
                        User research, interface design
                    </div>

                    <div class="keyword-item">
                        <strong>Wireframing & Prototyping</strong><br>
                        Wireframes, prototypes, user flows
                    </div>

                    <div class="keyword-item">
                        <strong>Brand Identity</strong><br>
                        Branding, visual identity
                    </div>

                    <div class="keyword-item">
                        <strong>Visual Communication</strong><br>
                        Visual storytelling, communication
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # DIVIDER
    # ========================================================

    st.html(
        """
        <div class="resources-divider"></div>
        """
    )


    # ========================================================
    # RESUME TEMPLATES
    # ========================================================

    st.html(
        """
        <div class="resources-section">

            <div class="resources-section-title">
                📄 ATS-Friendly Resume Templates
            </div>

            <div class="resources-section-description">
                Ready-to-use templates designed around
                ATS-friendly resume principles.
            </div>

        </div>
        """
    )


    st.html(
        """
        <div class="template-card">

            <div class="template-icon">
                📄
            </div>

            <div>

                <div class="template-title">
                    Resume templates are coming soon
                </div>

                <div class="template-description">
                    Downloadable ATS-optimized resume templates
                    will be available here in a future update.
                </div>

            </div>

        </div>
        """
    )