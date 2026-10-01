import streamlit as st


def _inject_landing_css() -> None:
    st.html(
        """
        <style>

        /* =========================================================
           GLOBAL PAGE
           ========================================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at 15% 15%,
                    rgba(99, 102, 241, 0.18),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 85% 20%,
                    rgba(168, 85, 247, 0.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 50% 100%,
                    rgba(79, 70, 229, 0.10),
                    transparent 35%
                ),
                #070a13 !important;

            color: #ffffff;
            overflow-x: hidden;
        }

        .main {
            background: transparent !important;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 1.2rem;
            padding-bottom: 4rem;
        }

        /* Hide Streamlit default UI */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        /* =========================================================
           ANIMATED BACKGROUND
           ========================================================= */

        .landing-background {
            position: fixed;
            inset: 0;
            z-index: -10;
            pointer-events: none;
            overflow: hidden;
        }

        .grid-background {
            position: absolute;
            inset: 0;

            background-image:
                linear-gradient(
                    rgba(129, 140, 248, 0.035) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(129, 140, 248, 0.035) 1px,
                    transparent 1px
                );

            background-size: 55px 55px;

            mask-image: radial-gradient(
                ellipse at center,
                black 15%,
                transparent 78%
            );

            -webkit-mask-image: radial-gradient(
                ellipse at center,
                black 15%,
                transparent 78%
            );
        }

        .glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.35;
        }

        .glow-one {
            width: 420px;
            height: 420px;
            background: #4f46e5;
            top: -180px;
            left: -100px;
            animation: floatOne 12s ease-in-out infinite;
        }

        .glow-two {
            width: 360px;
            height: 360px;
            background: #9333ea;
            right: -100px;
            top: 170px;
            animation: floatTwo 15s ease-in-out infinite;
        }

        .glow-three {
            width: 300px;
            height: 300px;
            background: #2563eb;
            left: 35%;
            bottom: -180px;
            opacity: 0.18;
            animation: floatThree 13s ease-in-out infinite;
        }

        @keyframes floatOne {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }

            50% {
                transform: translate(80px, 60px) scale(1.12);
            }
        }

        @keyframes floatTwo {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }

            50% {
                transform: translate(-70px, 80px) scale(1.15);
            }
        }

        @keyframes floatThree {
            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(60px, -50px);
            }
        }

        /* =========================================================
           NAVBAR
           ========================================================= */

        .landing-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;

            padding: 10px 4px 18px 4px;

            margin-bottom: 55px;
        }

        .landing-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .landing-brand-icon {
            width: 43px;
            height: 43px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #8b5cf6
                );

            box-shadow:
                0 10px 35px rgba(99, 102, 241, 0.30),
                inset 0 1px 1px rgba(255,255,255,0.25);

            color: white;
            font-size: 20px;
            font-weight: 800;
        }

        .landing-brand-name {
            color: #ffffff;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .landing-brand-name span {
            background:
                linear-gradient(
                    90deg,
                    #818cf8,
                    #c084fc
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .landing-brand-subtitle {
            color: #687187;
            font-size: 10px;
            margin-top: 1px;
        }

        .navbar-badge {
            padding: 7px 13px;
            border-radius: 999px;

            background: rgba(129,140,248,0.07);
            border: 1px solid rgba(129,140,248,0.14);

            color: #9ba3ff;
            font-size: 11px;
            font-weight: 600;
        }

        /* =========================================================
           HERO
           ========================================================= */

        .hero {
            position: relative;
            text-align: center;

            max-width: 930px;
            margin: 0 auto;

            padding: 35px 0 20px 0;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;

            padding: 8px 15px;
            margin-bottom: 22px;

            border-radius: 999px;

            background:
                rgba(99,102,241,0.08);

            border:
                1px solid rgba(129,140,248,0.18);

            color: #a5b4fc;

            font-size: 11px;
            font-weight: 700;

            box-shadow:
                0 0 30px rgba(99,102,241,0.07);
        }

        .hero-badge-dot {
            width: 6px;
            height: 6px;

            border-radius: 50%;

            background: #818cf8;

            box-shadow:
                0 0 10px #818cf8;

            animation: pulseDot 2s ease-in-out infinite;
        }

        @keyframes pulseDot {
            0%, 100% {
                opacity: 0.45;
                transform: scale(0.8);
            }

            50% {
                opacity: 1;
                transform: scale(1.15);
            }
        }

        .hero-title {
            margin: 0;

            color: #ffffff;

            font-size: clamp(46px, 7vw, 82px);

            line-height: 1.02;

            font-weight: 850;

            letter-spacing: -3.5px;

            text-shadow:
                0 15px 50px rgba(0,0,0,0.35);
        }

        .hero-gradient-text {
            background:
                linear-gradient(
                    90deg,
                    #818cf8 0%,
                    #a78bfa 45%,
                    #c084fc 100%
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            background-size: 200% auto;

            animation: gradientMove 5s ease-in-out infinite;
        }

        @keyframes gradientMove {
            0%, 100% {
                background-position: 0% center;
            }

            50% {
                background-position: 100% center;
            }
        }

        .hero-description {
            max-width: 720px;

            margin: 25px auto 0 auto;

            color: #8d96aa;

            font-size: 15px;

            line-height: 1.8;
        }

        /* =========================================================
           CTA BUTTON AREA
           ========================================================= */

        .hero-cta {
            margin-top: 32px;

            display: flex;
            justify-content: center;
            gap: 12px;
        }

        /* =========================================================
           TRUST
           ========================================================= */

        .trust-row {
            margin-top: 38px;

            display: flex;
            justify-content: center;
            align-items: center;
            gap: 22px;

            color: #60697d;
            font-size: 11px;
        }

        .trust-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .trust-check {
            color: #818cf8;
        }

        /* =========================================================
           PRODUCT PREVIEW
           ========================================================= */

        .preview-wrapper {
            max-width: 1000px;

            margin: 75px auto 0 auto;

            position: relative;
        }

        .preview-glow {
            position: absolute;
            inset: -30px;

            background:
                radial-gradient(
                    ellipse at center,
                    rgba(99,102,241,0.18),
                    transparent 65%
                );

            filter: blur(25px);

            z-index: -1;
        }

        .preview-window {
            overflow: hidden;

            border-radius: 20px;

            background:
                rgba(12,16,29,0.90);

            border:
                1px solid rgba(255,255,255,0.09);

            box-shadow:
                0 35px 100px rgba(0,0,0,0.48),
                inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .preview-topbar {
            height: 43px;

            display: flex;
            align-items: center;

            padding: 0 16px;

            background:
                rgba(255,255,255,0.025);

            border-bottom:
                1px solid rgba(255,255,255,0.055);
        }

        .window-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;

            margin-right: 6px;

            background: #30364a;
        }

        .window-title {
            margin-left: 12px;

            color: #5f687c;

            font-size: 10px;
        }

        .preview-content {
            display: grid;

            grid-template-columns:
                190px 1fr;

            min-height: 320px;
        }

        .preview-sidebar {
            padding: 22px 15px;

            background:
                rgba(255,255,255,0.018);

            border-right:
                1px solid rgba(255,255,255,0.055);
        }

        .preview-logo {
            color: #ffffff;

            font-size: 13px;

            font-weight: 750;

            margin-bottom: 25px;
        }

        .preview-nav {
            padding: 9px 10px;

            margin-bottom: 6px;

            border-radius: 8px;

            color: #6f7890;

            font-size: 10px;
        }

        .preview-nav.active {
            color: #b5bcff;

            background:
                rgba(99,102,241,0.10);

            border:
                1px solid rgba(99,102,241,0.08);
        }

        .preview-main {
            padding: 28px;
        }

        .preview-heading {
            color: #ffffff;

            font-size: 18px;

            font-weight: 750;

            margin-bottom: 5px;
        }

        .preview-subheading {
            color: #697287;

            font-size: 10px;

            margin-bottom: 22px;
        }

        .score-grid {
            display: grid;

            grid-template-columns:
                1.1fr 1fr 1fr 1fr;

            gap: 10px;
        }

        .score-card {
            padding: 16px;

            border-radius: 12px;

            background:
                rgba(255,255,255,0.025);

            border:
                1px solid rgba(255,255,255,0.055);
        }

        .score-label {
            color: #687187;

            font-size: 9px;

            margin-bottom: 7px;
        }

        .score-value {
            color: #ffffff;

            font-size: 21px;

            font-weight: 800;
        }

        .score-main {
            background:
                linear-gradient(
                    145deg,
                    rgba(99,102,241,0.15),
                    rgba(139,92,246,0.05)
                );

            border-color:
                rgba(129,140,248,0.15);
        }

        .score-main .score-value {
            color: #a5b4fc;
        }

        .preview-progress {
            margin-top: 18px;

            height: 7px;

            border-radius: 99px;

            background: #1a2031;

            overflow: hidden;
        }

        .preview-progress-fill {
            height: 100%;

            width: 81%;

            border-radius: 99px;

            background:
                linear-gradient(
                    90deg,
                    #6366f1,
                    #a78bfa
                );

            box-shadow:
                0 0 18px rgba(129,140,248,0.3);
        }

        .preview-bottom {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 10px;

            margin-top: 10px;
        }

        .mini-card {
            height: 65px;

            padding: 12px;

            border-radius: 10px;

            background:
                rgba(255,255,255,0.022);

            border:
                1px solid rgba(255,255,255,0.045);
        }

        /* =========================================================
           SECTION HEADINGS
           ========================================================= */

        .section {
            max-width: 1050px;

            margin: 110px auto 0 auto;

            text-align: center;
        }

        .section-eyebrow {
            color: #818cf8;

            font-size: 10px;

            font-weight: 800;

            text-transform: uppercase;

            letter-spacing: 1.6px;

            margin-bottom: 10px;
        }

        .section-title {
            color: #ffffff;

            font-size: 30px;

            font-weight: 800;

            letter-spacing: -1px;

            margin-bottom: 10px;
        }

        .section-description {
            color: #777f94;

            font-size: 13px;

            max-width: 620px;

            margin: 0 auto;

            line-height: 1.7;
        }

        /* =========================================================
           FEATURE CARDS
           ========================================================= */

        .feature-grid {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 13px;

            margin-top: 35px;

            text-align: left;
        }

        .feature-card {
            position: relative;

            padding: 23px;

            min-height: 175px;

            border-radius: 17px;

            background:
                linear-gradient(
                    145deg,
                    rgba(20,25,45,0.80),
                    rgba(11,15,28,0.80)
                );

            border:
                1px solid rgba(255,255,255,0.065);

            transition:
                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);

            border-color:
                rgba(129,140,248,0.25);

            box-shadow:
                0 20px 45px rgba(0,0,0,0.25);
        }

        .feature-icon {
            width: 40px;
            height: 40px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 11px;

            background:
                rgba(99,102,241,0.10);

            border:
                1px solid rgba(129,140,248,0.10);

            font-size: 19px;

            margin-bottom: 17px;
        }

        .feature-title {
            color: #ffffff;

            font-size: 14px;

            font-weight: 700;

            margin-bottom: 7px;
        }

        .feature-text {
            color: #727c91;

            font-size: 11px;

            line-height: 1.65;
        }

        /* =========================================================
           WORKFLOW
           ========================================================= */

        .workflow-grid {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 13px;

            margin-top: 35px;

            text-align: left;
        }

        .workflow-card {
            padding: 23px;

            border-radius: 17px;

            background:
                rgba(17,21,38,0.65);

            border:
                1px solid rgba(255,255,255,0.055);
        }

        .workflow-number {
            color: #818cf8;

            font-size: 10px;

            font-weight: 800;

            letter-spacing: 1.2px;

            margin-bottom: 17px;
        }

        .workflow-title {
            color: #ffffff;

            font-size: 15px;

            font-weight: 700;

            margin-bottom: 7px;
        }

        .workflow-text {
            color: #737d91;

            font-size: 11px;

            line-height: 1.6;
        }

        /* =========================================================
           FINAL CTA
           ========================================================= */

        .final-cta {
            position: relative;

            overflow: hidden;

            max-width: 950px;

            margin: 110px auto 0 auto;

            padding: 55px 30px;

            text-align: center;

            border-radius: 25px;

            background:
                radial-gradient(
                    circle at center top,
                    rgba(99,102,241,0.17),
                    transparent 60%
                ),
                rgba(16,20,37,0.75);

            border:
                1px solid rgba(129,140,248,0.11);

            box-shadow:
                0 25px 70px rgba(0,0,0,0.25);
        }

        .final-cta-title {
            color: #ffffff;

            font-size: 29px;

            font-weight: 800;

            letter-spacing: -0.8px;

            margin-bottom: 10px;
        }

        .final-cta-text {
            color: #7d869a;

            font-size: 13px;

            margin-bottom: 25px;
        }

        /* =========================================================
           FOOTER
           ========================================================= */

        .landing-footer {
            max-width: 1050px;

            margin: 70px auto 0 auto;

            padding-top: 25px;

            border-top:
                1px solid rgba(255,255,255,0.055);

            display: flex;

            justify-content: space-between;

            color: #50596d;

            font-size: 10px;
        }

        /* =========================================================
        STREAMLIT BUTTONS
        ========================================================= */

        .stButton > button {
            border-radius: 11px !important;
            min-height: 44px !important;
            font-weight: 650 !important;
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease,
                background 0.2s ease !important;
        }

        /* Primary buttons */

        .stButton > button[kind="primary"] {
            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #7c3aed
                ) !important;

            color: #ffffff !important;

            border: 1px solid rgba(129,140,248,0.55) !important;

            box-shadow:
                0 8px 25px rgba(99,102,241,0.20) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background:
                linear-gradient(
                    135deg,
                    #7174ff,
                    #8b5cf6
                ) !important;

            transform: translateY(-2px) !important;

            box-shadow:
                0 12px 32px rgba(99,102,241,0.32) !important;
        }

        /* Secondary buttons */

        .stButton > button[kind="secondary"] {
            background:
                rgba(255,255,255,0.035) !important;

            color: #c7cbe0 !important;

            border:
                1px solid rgba(255,255,255,0.12) !important;

            box-shadow:
                none !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background:
                rgba(129,140,248,0.08) !important;

            color: #ffffff !important;

            border-color:
                rgba(129,140,248,0.35) !important;

            transform: translateY(-2px) !important;

            box-shadow:
                0 8px 25px rgba(99,102,241,0.10) !important;
        }
        /* =========================================================
           MOBILE
           ========================================================= */

        @media (max-width: 800px) {

            .hero-title {
                font-size: 46px;
                letter-spacing: -2px;
            }

            .feature-grid,
            .workflow-grid {
                grid-template-columns: 1fr;
            }

            .preview-content {
                grid-template-columns: 1fr;
            }

            .preview-sidebar {
                display: none;
            }

            .score-grid {
                grid-template-columns: 1fr 1fr;
            }

            .landing-navbar {
                margin-bottom: 30px;
            }

            .navbar-badge {
                display: none;
            }

            .trust-row {
                flex-wrap: wrap;
            }

            .landing-footer {
                flex-direction: column;
                gap: 8px;
            }
        }

        </style>
        """,
        
    )


def _navigate(view: str) -> None:
    st.session_state["current_view"] = view
    st.rerun()


def render() -> None:

    _inject_landing_css()

    # =========================================================
    # ANIMATED BACKGROUND
    # =========================================================

    st.html(
        """
        <div class="landing-background">

            <div class="grid-background"></div>

            <div class="glow glow-one"></div>

            <div class="glow glow-two"></div>

            <div class="glow glow-three"></div>

        </div>
        """,
        
    )

    # =========================================================
    # NAVBAR
    # =========================================================

    st.html(
        """
        <div class="landing-navbar">

            <div class="landing-brand">

                <div class="landing-brand-icon">
                    ✦
                </div>

                <div>
                    <div class="landing-brand-name">
                        HireMind <span>AI</span>
                    </div>

                    <div class="landing-brand-subtitle">
                        Resume Intelligence
                    </div>
                </div>

            </div>

            <div class="navbar-badge">
                AI-POWERED RESUME ANALYSIS
            </div>

        </div>
        """,
        
    )

    # =========================================================
    # HERO
    # =========================================================

    st.html(
        """
        <section class="hero">

            <div class="hero-badge">
                <span class="hero-badge-dot"></span>
                AI-POWERED RESUME INTELLIGENCE
            </div>

            <h1 class="hero-title">
                Build a resume
                <br>
                that <span class="hero-gradient-text">
                gets noticed.
                </span>
            </h1>

            <p class="hero-description">
                Analyze your resume against real job descriptions,
                understand your ATS performance, discover skill gaps,
                and get actionable recommendations powered by AI.
            </p>

        </section>
        """,
        
    )

    # =========================================================
    # HERO BUTTONS
    # =========================================================

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        left, right = st.columns(2)

        with left:

            if st.button(
                "🚀 Get Started",
                type="primary",
                use_container_width=True,
                key="landing_get_started",
            ):
                _navigate("signup")

        with right:

            if st.button(
                "Sign In →",
                use_container_width=True,
                key="landing_sign_in",
            ):
                _navigate("login")

    # =========================================================
    # TRUST ROW
    # =========================================================

    st.html(
        """
        <div class="trust-row">

            <div class="trust-item">
                <span class="trust-check">✓</span>
                ATS scoring
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                Job matching
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                Skill validation
            </div>

            <div class="trust-item">
                <span class="trust-check">✓</span>
                AI recommendations
            </div>

        </div>
        """,
        
    )

    # =========================================================
    # PRODUCT PREVIEW
    # =========================================================

    st.html(
        """
        <div class="preview-wrapper">

            <div class="preview-glow"></div>

            <div class="preview-window">

                <div class="preview-topbar">

                    <span class="window-dot"></span>
                    <span class="window-dot"></span>
                    <span class="window-dot"></span>

                    <span class="window-title">
                        HireMind AI · Resume Analysis
                    </span>

                </div>

                <div class="preview-content">

                    <div class="preview-sidebar">

                        <div class="preview-logo">
                            HireMind AI
                        </div>

                        <div class="preview-nav active">
                            ◈ Dashboard
                        </div>

                        <div class="preview-nav">
                            ✦ Analyze Resume
                        </div>

                        <div class="preview-nav">
                            ◷ History
                        </div>

                        <div class="preview-nav">
                            ▣ Resources
                        </div>

                    </div>

                    <div class="preview-main">

                        <div class="preview-heading">
                            Resume Performance
                        </div>

                        <div class="preview-subheading">
                            AI-powered ATS analysis
                        </div>

                        <div class="score-grid">

                            <div class="score-card score-main">

                                <div class="score-label">
                                    ATS SCORE
                                </div>

                                <div class="score-value">
                                    81.0
                                </div>

                            </div>

                            <div class="score-card">

                                <div class="score-label">
                                    KEYWORDS
                                </div>

                                <div class="score-value">
                                    87%
                                </div>

                            </div>

                            <div class="score-card">

                                <div class="score-label">
                                    CONTENT
                                </div>

                                <div class="score-value">
                                    76%
                                </div>

                            </div>

                            <div class="score-card">

                                <div class="score-label">
                                    JD MATCH
                                </div>

                                <div class="score-value">
                                    78%
                                </div>

                            </div>

                        </div>

                        <div class="preview-progress">
                            <div class="preview-progress-fill"></div>
                        </div>

                        <div class="preview-bottom">

                            <div class="mini-card"></div>

                            <div class="mini-card"></div>

                        </div>

                    </div>

                </div>

            </div>

        </div>
        """,
        
    )

    # =========================================================
    # FEATURES
    # =========================================================

    st.html(
        """
        <div class="section">

            <div class="section-eyebrow">
                WHAT YOU GET
            </div>

            <div class="section-title">
                Your resume, analyzed by AI.
            </div>

            <div class="section-description">
                HireMind AI combines NLP, semantic matching,
                skill validation, and ATS-focused analysis to
                give you a deeper understanding of your resume.
            </div>

            <div class="feature-grid">

                <div class="feature-card">

                    <div class="feature-icon">
                        🎯
                    </div>

                    <div class="feature-title">
                        ATS Score
                    </div>

                    <div class="feature-text">
                        Understand your resume's performance
                        across formatting, keywords, content,
                        skills, and ATS compatibility.
                    </div>

                </div>

                <div class="feature-card">

                    <div class="feature-icon">
                        🔎
                    </div>

                    <div class="feature-title">
                        Job Description Matching
                    </div>

                    <div class="feature-text">
                        Compare your resume against a target
                        job description using keyword and
                        semantic signals.
                    </div>

                </div>

                <div class="feature-card">

                    <div class="feature-icon">
                        🧠
                    </div>

                    <div class="feature-title">
                        Skill Validation
                    </div>

                    <div class="feature-text">
                        See which skills have supporting evidence
                        in your projects and experience.
                    </div>

                </div>

                <div class="feature-card">

                    <div class="feature-icon">
                        💡
                    </div>

                    <div class="feature-title">
                        Smart Recommendations
                    </div>

                    <div class="feature-text">
                        Get practical recommendations to improve
                        weak areas of your resume.
                    </div>

                </div>

                <div class="feature-card">

                    <div class="feature-icon">
                        📊
                    </div>

                    <div class="feature-title">
                        Detailed Reports
                    </div>

                    <div class="feature-text">
                        Explore strengths, issues, missing keywords,
                        skill gaps, and detailed feedback.
                    </div>

                </div>

                <div class="feature-card">

                    <div class="feature-icon">
                        ⚡
                    </div>

                    <div class="feature-title">
                        Fast Analysis
                    </div>

                    <div class="feature-text">
                        Upload your resume and quickly turn it
                        into a structured AI-powered report.
                    </div>

                </div>

            </div>

        </div>
        """,
        
    )

    # =========================================================
    # WORKFLOW
    # =========================================================

    st.html(
        """
        <div class="section">

            <div class="section-eyebrow">
                SIMPLE WORKFLOW
            </div>

            <div class="section-title">
                From resume to insights in three steps.
            </div>

            <div class="workflow-grid">

                <div class="workflow-card">

                    <div class="workflow-number">
                        STEP 01
                    </div>

                    <div class="workflow-title">
                        Upload your resume
                    </div>

                    <div class="workflow-text">
                        Upload your PDF, DOC, or DOCX resume
                        and optionally add the job description
                        you're targeting.
                    </div>

                </div>

                <div class="workflow-card">

                    <div class="workflow-number">
                        STEP 02
                    </div>

                    <div class="workflow-title">
                        Let AI analyze it
                    </div>

                    <div class="workflow-text">
                        HireMind AI evaluates your resume using
                        NLP, semantic similarity, keyword matching,
                        and skill validation.
                    </div>

                </div>

                <div class="workflow-card">

                    <div class="workflow-number">
                        STEP 03
                    </div>

                    <div class="workflow-title">
                        Improve with confidence
                    </div>

                    <div class="workflow-text">
                        Use your personalized report to identify
                        gaps and make targeted improvements.
                    </div>

                </div>

            </div>

        </div>
        """,
        
    )

    # =========================================================
    # FINAL CTA
    # =========================================================

    st.html(
        """
        <div class="final-cta">

            <div class="final-cta-title">
                Ready to see what your resume is missing?
            </div>

            <div class="final-cta-text">
                Start your first AI-powered resume analysis.
            </div>

        </div>
        """,
        
    )

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:

        if st.button(
            "🚀 Analyze My Resume",
            type="primary",
            use_container_width=True,
            key="landing_bottom_cta",
        ):
            _navigate("signup")

    # =========================================================
    # FOOTER
    # =========================================================

    st.html(
        """
        <div class="landing-footer">

            <div>
                © 2026 HireMind AI
            </div>

            <div>
                AI Resume Intelligence
            </div>

        </div>
        """,
        
    )