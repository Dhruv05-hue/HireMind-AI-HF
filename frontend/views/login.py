import streamlit as st
from frontend.services import supabase_client


def _inject_login_css() -> None:
    st.html(
        """
        <style>
        /* ---------- Page ---------- */

        .stApp {
            background:
                radial-gradient(
                    circle at 15% 15%,
                    rgba(99, 102, 241, 0.16),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 85% 25%,
                    rgba(139, 92, 246, 0.12),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #080b16 0%,
                    #0d1020 50%,
                    #080b16 100%
                );
        }

        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        /* ---------- Brand ---------- */

        .login-brand {
            text-align: center;
            margin-bottom: 2rem;
        }

        .brand-icon {
            width: 58px;
            height: 58px;
            margin: 0 auto 14px auto;
            border-radius: 17px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            box-shadow:
                0 12px 35px rgba(99, 102, 241, 0.30),
                inset 0 1px 1px rgba(255,255,255,0.25);
            font-size: 27px;
        }

        .brand-name {
            color: #ffffff;
            font-size: 29px;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 4px;
        }

        .brand-name span {
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-tagline {
            color: #8b93a7;
            font-size: 14px;
        }

        /* ---------- Main Card ---------- */

        .login-card {
            max-width: 470px;
            margin: 0 auto;
            padding: 38px 38px 32px 38px;
            border-radius: 25px;
            background: rgba(17, 21, 38, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow:
                0 30px 80px rgba(0, 0, 0, 0.42),
                inset 0 1px 0 rgba(255,255,255,0.04);
            backdrop-filter: blur(18px);
        }

        .login-title {
            color: #ffffff;
            font-size: 27px;
            font-weight: 750;
            text-align: center;
            margin-bottom: 7px;
            letter-spacing: -0.7px;
        }

        .login-subtitle {
            color: #8e96aa;
            text-align: center;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 25px;
        }

        /* ---------- Inputs ---------- */

        div[data-testid="stTextInput"] label {
            color: #b9c0d0 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stTextInput"] input {
            background: #0d1120 !important;
            color: #ffffff !important;
            border: 1px solid #252b40 !important;
            border-radius: 12px !important;
            padding: 13px 14px !important;
            min-height: 48px !important;
            transition: all 0.2s ease;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #6366f1 !important;
            box-shadow:
                0 0 0 2px rgba(99,102,241,0.15) !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #555d70 !important;
        }

        /* ---------- Buttons ---------- */

        .stButton > button {
            width: 100% !important;
            min-height: 47px !important;
            border-radius: 12px !important;
            font-weight: 650 !important;

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

            color: #ffffff !important;

            border:
                1px solid rgba(129,140,248,0.55) !important;

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

            color: #ffffff !important;

            transform: translateY(-2px) !important;

            box-shadow:
                0 12px 32px rgba(99,102,241,0.32) !important;
        }

        .stButton > button:not([kind="primary"]) {
            background:
                rgba(255,255,255,0.035) !important;

            color: #c7cbe0 !important;

            border:
                1px solid rgba(255,255,255,0.10) !important;

            box-shadow: none !important;
        }

        .stButton > button:not([kind="primary"]):hover {
            background:
                rgba(129,140,248,0.09) !important;

            color: #ffffff !important;

            border-color:
                rgba(129,140,248,0.35) !important;

            transform: translateY(-2px) !important;

            box-shadow:
                0 8px 25px rgba(99,102,241,0.10) !important;
        }

        /* ---------- Divider ---------- */

        .divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 22px 0;
            color: #60687b;
            font-size: 12px;
        }

        .divider::before,
        .divider::after {
            content: "";
            height: 1px;
            flex: 1;
            background: #252b3d;
        }

        /* ---------- Footer ---------- */

        .login-footer {
            text-align: center;
            margin-top: 24px;
            color: #70788c;
            font-size: 13px;
        }

        .security-note {
            text-align: center;
            color: #596174;
            font-size: 11px;
            margin-top: 19px;
        }

        /* ---------- Feature Strip ---------- */

        .feature-strip {
            max-width: 850px;
            margin: 35px auto 0 auto;
            display: flex;
            justify-content: center;
            gap: 14px;
            flex-wrap: wrap;
        }

        .feature-pill {
            padding: 9px 15px;
            border-radius: 999px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.06);
            color: #8991a5;
            font-size: 12px;
        }

        .feature-pill span {
            color: #a5b4fc;
            margin-right: 5px;
        }

        /* ---------- Mobile ---------- */

        @media (max-width: 600px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .login-card {
                padding: 28px 20px 25px 20px;
            }

            .brand-name {
                font-size: 25px;
            }
        }
        </style>
        """
    )


def _go_to_signup() -> None:
    st.session_state["current_view"] = "signup"
    st.rerun()


def _go_to_landing() -> None:
    st.session_state["current_view"] = "landing"
    st.rerun()


def _handle_login(
    email: str,
    password: str,
) -> None:

    if not email.strip():
        st.error("Please enter your email address.")
        return

    if not password:
        st.error("Please enter your password.")
        return

    with st.spinner("Signing you in..."):
        result = supabase_client.sign_in_with_password(
            email.strip(),
            password,
        )

    if result.get("error"):
        st.error(result["error"])
        return

    # ---------------------------------------------------------
    # Store authenticated session
    # ---------------------------------------------------------

    st.session_state["access_token"] = result.get(
        "access_token"
    )

    st.session_state["refresh_token"] = result.get(
        "refresh_token"
    )

    st.session_state["user_id"] = result.get(
        "user_id"
    )

    st.session_state["user_email"] = (
        result.get("email")
        or email.strip()
    )

    # ---------------------------------------------------------
    # Store username
    # ---------------------------------------------------------

    username = (
        result.get("username")
        or ""
    ).strip()

    st.session_state["username"] = username

    # ---------------------------------------------------------
    # Clear authentication messages
    # ---------------------------------------------------------

    st.session_state["auth_error"] = None
    st.session_state["auth_info"] = None

    # ---------------------------------------------------------
    # Go to authenticated dashboard
    # ---------------------------------------------------------

    st.session_state["current_view"] = "dashboard"

    st.rerun()


def render() -> None:
    _inject_login_css()

    # ---------- Brand ----------

    st.html(
        """
        <div class="login-brand">

            <div class="brand-icon">
                ✦
            </div>

            <div class="brand-name">
                HireMind <span>AI</span>
            </div>

            <div class="brand-tagline">
                Intelligent resume analysis for your next opportunity
            </div>

        </div>
        """
    )

    # ---------- Login Card Header ----------

    st.html(
        """
        <div class="login-card">

            <div class="login-title">
                Welcome back
            </div>

            <div class="login-subtitle">
                Sign in to analyze your resume, track your ATS score,
                and improve your chances of getting noticed.
            </div>

        </div>
        """
    )

    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="login_email",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password",
    )

    st.html(
        "<div style='height: 8px'></div>"
    )

    if st.button(
        "Sign in to HireMind AI  →",
        type="primary",
        use_container_width=True,
        key="login_button",
    ):
        _handle_login(
            email,
            password,
        )

    st.html(
        '<div class="google-info">'
        'Secure authentication powered by Supabase'
        '</div>'
    )

    st.html(
        """
        <div class="login-footer">
            Don't have an account?
        </div>
        """
    )

    if st.button(
        "Create a free account",
        use_container_width=True,
        key="signup_link",
    ):
        _go_to_signup()

    if st.button(
        "← Back to home",
        use_container_width=True,
        key="back_home",
    ):
        _go_to_landing()

    st.html(
        """
        <div class="security-note">
            🔒 Your authentication is handled securely by Supabase.
        </div>
        """
    )

    # ---------- Feature Strip ----------

    st.html(
        """
        <div class="feature-strip">

            <div class="feature-pill">
                <span>✓</span>
                ATS scoring
            </div>

            <div class="feature-pill">
                <span>✓</span>
                JD matching
            </div>

            <div class="feature-pill">
                <span>✓</span>
                Skill gap analysis
            </div>

            <div class="feature-pill">
                <span>✓</span>
                Detailed feedback
            </div>

        </div>
        """
    )