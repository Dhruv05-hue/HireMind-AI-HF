import streamlit as st
from frontend.services import supabase_client


def _inject_signup_css() -> None:
    st.html(
        """
        <style>
        /* ---------- Page ---------- */

        .stApp {
            background:
                radial-gradient(
                    circle at 12% 18%,
                    rgba(99, 102, 241, 0.17),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 88% 22%,
                    rgba(168, 85, 247, 0.13),
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

        .signup-brand {
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

        .signup-card {
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

        .signup-title {
            color: #ffffff;
            font-size: 27px;
            font-weight: 750;
            text-align: center;
            margin-bottom: 7px;
            letter-spacing: -0.7px;
        }

        .signup-subtitle {
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
            width: 100%;
            min-height: 47px;
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

        .stButton > button[kind="secondary"] {
            background:
                rgba(255,255,255,0.035) !important;

            color: #c7cbe0 !important;

            border:
                1px solid rgba(255,255,255,0.10) !important;

            box-shadow: none !important;
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

        /* ---------- Password Requirements ---------- */

        .password-box {
            margin-top: 8px;
            margin-bottom: 17px;
            padding: 13px 15px;
            border-radius: 12px;
            background: rgba(255,255,255,0.025);
            border: 1px solid rgba(255,255,255,0.055);
        }

        .password-title {
            color: #aeb6c8;
            font-size: 12px;
            font-weight: 650;
            margin-bottom: 8px;
        }

        .password-rule {
            color: #737c91;
            font-size: 11px;
            margin: 4px 0;
        }

        .password-rule.valid {
            color: #86efac;
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

        .signup-footer {
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

        /* ---------- Benefits ---------- */

        .benefit-strip {
            max-width: 850px;
            margin: 35px auto 0 auto;
            display: flex;
            justify-content: center;
            gap: 14px;
            flex-wrap: wrap;
        }

        .benefit-pill {
            padding: 9px 15px;
            border-radius: 999px;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.06);
            color: #8991a5;
            font-size: 12px;
        }

        .benefit-pill span {
            color: #a5b4fc;
            margin-right: 5px;
        }

        /* ---------- Mobile ---------- */

        @media (max-width: 600px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .signup-card {
                padding: 28px 20px 25px 20px;
            }

            .brand-name {
                font-size: 25px;
            }
        }
        </style>
        """
    )


def _go_to_login() -> None:
    st.session_state["current_view"] = "login"
    st.rerun()


def _go_to_landing() -> None:
    st.session_state["current_view"] = "landing"
    st.rerun()


def _password_rules(password: str) -> None:
    length_valid = len(password) >= 6
    has_number = any(char.isdigit() for char in password)
    has_letter = any(char.isalpha() for char in password)

    length_class = "valid" if length_valid else ""
    number_class = "valid" if has_number else ""
    letter_class = "valid" if has_letter else ""

    length_icon = "✓" if length_valid else "○"
    number_icon = "✓" if has_number else "○"
    letter_icon = "✓" if has_letter else "○"

    st.html(
        f"""
        <div class="password-box">
            <div class="password-title">
                Password requirements
            </div>

            <div class="password-rule {length_class}">
                {length_icon} At least 6 characters
            </div>

            <div class="password-rule {letter_class}">
                {letter_icon} Contains a letter
            </div>

            <div class="password-rule {number_class}">
                {number_icon} Contains a number
            </div>
        </div>
        """
    )


def _handle_signup(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> None:

    username = username.strip()
    email = email.strip()

    if not username:
        st.error("Please choose a username.")
        return

    if len(username) < 3:
        st.error("Username must contain at least 3 characters.")
        return

    if not email:
        st.error("Please enter your email address.")
        return

    if not password:
        st.error("Please create a password.")
        return

    if len(password) < 6:
        st.error("Password must contain at least 6 characters.")
        return

    if not any(char.isalpha() for char in password):
        st.error("Password must contain at least one letter.")
        return

    if not any(char.isdigit() for char in password):
        st.error("Password must contain at least one number.")
        return

    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    with st.spinner("Creating your HireMind AI account..."):
        result = supabase_client.sign_up_with_password(
            username,
            email,
            password,
        )

    if result.get("error"):
        st.error(result["error"])
        return

    # Supabase may require email confirmation before
    # returning an authenticated session.
    if result.get("pending_confirmation"):
        st.session_state["auth_info"] = (
            f"Your account has been created. "
            f"Please check {email} and verify your email address "
            f"before signing in."
        )

        st.session_state["current_view"] = "login"
        st.rerun()

    # Some Supabase configurations immediately return
    # an authenticated session after signup.
    if result.get("access_token"):
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
            or email
        )

        st.session_state["username"] = (
            result.get("username")
            or username
        )

        st.session_state["auth_error"] = None
        st.session_state["auth_info"] = None
        st.session_state["current_view"] = "dashboard"

        st.rerun()

    st.session_state["auth_info"] = (
        "Account created successfully. "
        "Please sign in to continue."
    )

    st.session_state["current_view"] = "login"
    st.rerun()


def render() -> None:
    _inject_signup_css()

    # ---------- Brand ----------

    st.html(
        """
        <div class="signup-brand">
            <div class="brand-icon">✦</div>

            <div class="brand-name">
                HireMind <span>AI</span>
            </div>

            <div class="brand-tagline">
                Build a resume that gets noticed
            </div>
        </div>
        """
    )

    # ---------- Signup Card ----------

    st.html(
        """
        <div class="signup-card">
            <div class="signup-title">
                Create your account
            </div>

            <div class="signup-subtitle">
                Start analyzing your resume with AI-powered ATS
                scoring, job matching, and personalized
                recommendations.
            </div>
        </div>
        """
    )

    # ---------- Username ----------

    username = st.text_input(
        "Username",
        placeholder="Choose a username",
        key="signup_username",
    )

    # ---------- Email ----------

    email = st.text_input(
        "Email address",
        placeholder="you@example.com",
        key="signup_email",
    )

    # ---------- Password ----------

    password = st.text_input(
        "Create password",
        type="password",
        placeholder="Create a secure password",
        key="signup_password",
    )

    _password_rules(password)

    # ---------- Confirm Password ----------

    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Re-enter your password",
        key="signup_confirm_password",
    )

    st.html(
        "<div style='height: 6px'></div>"
    )

    # ---------- Create Account ----------

    if st.button(
        "Create my HireMind AI account  →",
        type="primary",
        use_container_width=True,
        key="signup_button",
    ):
        _handle_signup(
            username,
            email,
            password,
            confirm_password,
        )

    # ---------- Divider ----------

    st.html(
        '<div class="divider">OR</div>'
    )

    st.html(
        '<div class="google-info">'
        'Secure authentication powered by Supabase'
        '</div>'
    )

    # ---------- Login Link ----------

    st.html(
        """
        <div class="signup-footer">
            Already have an account?
        </div>
        """
    )

    if st.button(
        "Sign in instead",
        use_container_width=True,
        key="login_link",
    ):
        _go_to_login()

    if st.button(
        "← Back to home",
        use_container_width=True,
        key="back_home",
    ):
        _go_to_landing()

    st.html(
        """
        <div class="security-note">
            🔒 Your account is securely managed by Supabase.
        </div>
        """
    )

    # ---------- Benefits ----------

    st.html(
        """
        <div class="benefit-strip">

            <div class="benefit-pill">
                <span>✦</span>
                AI-powered analysis
            </div>

            <div class="benefit-pill">
                <span>✓</span>
                ATS compatibility
            </div>

            <div class="benefit-pill">
                <span>⌁</span>
                Job description matching
            </div>

            <div class="benefit-pill">
                <span>↗</span>
                Career insights
            </div>

        </div>
        """
    )