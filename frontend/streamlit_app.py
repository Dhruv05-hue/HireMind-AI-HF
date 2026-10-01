import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HireMind AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

SESSION_DEFAULTS = {
    "access_token": None,
    "refresh_token": None,
    "user_id": None,
    "user_email": None,
    "auth_error": None,
    "auth_info": None,
    "current_view": "landing",
}

for key, default in SESSION_DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = default


# ============================================================
# LOAD MAIN CSS
# ============================================================

def load_css():

    possible_paths = [
        Path(__file__).parent / "assets" / "style.css",
        Path(__file__).parent / "assets" / "styles.css",
    ]

    for css_path in possible_paths:

        if css_path.exists():

            try:

                return (
                    f"<style>"
                    f"{css_path.read_text(encoding='utf-8')}"
                    f"</style>"
                )

            except Exception:
                return ""

    return ""


st.html(load_css())


# ============================================================
# GLOBAL UI FIXES
# ============================================================

def inject_global_ui_css():

    st.html(
        """
        <style>

        /* ====================================================
           GLOBAL APP
           ==================================================== */

        html,
        body {

            background:
                #070a13 !important;
        }


        .stApp {

            background:
                radial-gradient(
                    circle at 10% 5%,
                    rgba(99,102,241,0.08),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 90% 8%,
                    rgba(139,92,246,0.08),
                    transparent 30%
                ),
                linear-gradient(
                    180deg,
                    #090c18 0%,
                    #060810 100%
                ) !important;

            color:
                #ffffff !important;
        }


        [data-testid="stAppViewContainer"] {

            background:
                transparent !important;
        }


        [data-testid="stMain"] {

            background:
                transparent !important;
        }


        .main {

            background:
                transparent !important;
        }


        /* ====================================================
           REMOVE STREAMLIT TOP HEADER / WHITE SPACE
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

            display:
                none !important;
        }


        #MainMenu {

            visibility:
                hidden !important;
        }


        footer {

            visibility:
                hidden !important;
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
                1px solid
                rgba(255,255,255,0.10) !important;

            box-shadow:
                8px 0 35px
                rgba(0,0,0,0.24) !important;
        }


        [data-testid="stSidebar"] > div:first-child {

            background:
                transparent !important;
        }


        [data-testid="stSidebarContent"] {

            background:
                transparent !important;
        }


        /* ====================================================
           SIDEBAR BRAND
           ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-brand {

            display:
                flex;

            align-items:
                center;

            gap:
                11px;

            padding:
                8px 3px 5px 3px;
        }


        [data-testid="stSidebar"]
        .brand-icon {

            width:
                38px;

            height:
                38px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                11px;

            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #8b5cf6
                );

            color:
                #ffffff !important;

            font-size:
                17px;

            font-weight:
                800;

            box-shadow:
                0 7px 20px
                rgba(99,102,241,0.25);
        }


        [data-testid="stSidebar"]
        .brand-name {

            color:
                #ffffff !important;

            opacity:
                1 !important;

            font-size:
                14px !important;

            line-height:
                1.3 !important;

            font-weight:
                800 !important;
        }


        [data-testid="stSidebar"]
        .brand-subtitle {

            color:
                #aab3c7 !important;

            opacity:
                1 !important;

            font-size:
                10px !important;

            line-height:
                1.4 !important;
        }


        /* ====================================================
           SIDEBAR DIVIDER
           ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-divider {

            height:
                1px;

            margin:
                17px 0 19px 0;

            background:
                rgba(255,255,255,0.07);
        }


        /* ====================================================
           SIDEBAR SECTION TITLES
           ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-section-title {

            color:
                #b9c2d5 !important;

            opacity:
                1 !important;

            font-size:
                10px !important;

            font-weight:
                800 !important;

            letter-spacing:
                1.3px !important;

            line-height:
                1.5 !important;

            text-transform:
                uppercase !important;

            margin:
                14px 0 9px 0;
        }


        /* ====================================================
           SIDEBAR NAVIGATION BUTTONS
           ==================================================== */

        [data-testid="stSidebar"]
        .stButton {

            margin:
                0 0 8px 0 !important;
        }


        [data-testid="stSidebar"]
        .stButton > button {

            width:
                100% !important;

            min-height:
                42px !important;

            padding:
                0 14px !important;

            border-radius:
                10px !important;

            background:
                rgba(255,255,255,0.035) !important;

            border:
                1px solid
                rgba(255,255,255,0.11) !important;

            color:
                #e3e7f1 !important;

            opacity:
                1 !important;

            font-size:
                12px !important;

            font-weight:
                650 !important;

            box-shadow:
                none !important;

            transition:
                all 0.18s ease !important;
        }


        /* Button text */

        [data-testid="stSidebar"]
        .stButton > button p {

            color:
                #e3e7f1 !important;

            opacity:
                1 !important;

            font-size:
                12px !important;

            font-weight:
                650 !important;
        }


        [data-testid="stSidebar"]
        .stButton > button span {

            color:
                #e3e7f1 !important;

            opacity:
                1 !important;
        }


        /* Hover */

        [data-testid="stSidebar"]
        .stButton > button:hover {

            background:
                linear-gradient(
                    135deg,
                    rgba(99,102,241,0.16),
                    rgba(139,92,246,0.11)
                ) !important;

            border-color:
                rgba(129,140,248,0.40) !important;

            color:
                #ffffff !important;

            transform:
                translateY(-1px) !important;

            box-shadow:
                0 6px 18px
                rgba(0,0,0,0.15) !important;
        }


        [data-testid="stSidebar"]
        .stButton > button:hover p {

            color:
                #ffffff !important;

            opacity:
                1 !important;
        }


        [data-testid="stSidebar"]
        .stButton > button:hover span {

            color:
                #ffffff !important;

            opacity:
                1 !important;
        }


        /* ====================================================
           SIDEBAR USER
           ==================================================== */

        [data-testid="stSidebar"]
        .sidebar-user {

            display:
                flex;

            align-items:
                center;

            gap:
                10px;

            margin:
                3px 0 14px 0;

            padding:
                10px 2px;
        }


        [data-testid="stSidebar"]
        .sidebar-user-avatar {

            width:
                34px;

            height:
                34px;

            flex-shrink:
                0;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            border-radius:
                10px;

            background:
                linear-gradient(
                    135deg,
                    #6366f1,
                    #8b5cf6
                );

            color:
                #ffffff !important;

            font-size:
                13px;

            font-weight:
                800;

            box-shadow:
                0 5px 15px
                rgba(99,102,241,0.20);
        }


        [data-testid="stSidebar"]
        .sidebar-user-info {

            min-width:
                0;
        }


        [data-testid="stSidebar"]
        .sidebar-user-label {

            color:
                #aeb7cb !important;

            opacity:
                1 !important;

            font-size:
                10px !important;

            font-weight:
                650 !important;

            margin-bottom:
                2px;
        }


        [data-testid="stSidebar"]
        .sidebar-user-email {

            color:
                #eef0f6 !important;

            opacity:
                1 !important;

            font-size:
                11px !important;

            font-weight:
                600 !important;

            line-height:
                1.45 !important;

            overflow-wrap:
                anywhere !important;
        }


        /* ====================================================
           SIGN OUT
           ==================================================== */

        [data-testid="stSidebar"]
        #nav_logout {

            color:
                #dfe3ee !important;
        }


        /* ====================================================
           SIDEBAR SCROLLBAR
           ==================================================== */

        [data-testid="stSidebar"]::-webkit-scrollbar {

            width:
                5px;
        }


        [data-testid="stSidebar"]::-webkit-scrollbar-track {

            background:
                transparent;
        }


        [data-testid="stSidebar"]::-webkit-scrollbar-thumb {

            background:
                rgba(129,140,248,0.25);

            border-radius:
                10px;
        }


        /* ====================================================
           RESPONSIVE
           ==================================================== */

        @media (max-width: 700px) {

            [data-testid="stSidebar"]
            .brand-name {

                font-size:
                    13px !important;
            }

        }

        </style>
        """
    )


inject_global_ui_css()


# ============================================================
# SUPABASE AUTHENTICATION
# ============================================================

from frontend.services import supabase_client


# ============================================================
# GOOGLE OAUTH CALLBACK
# ============================================================

if (
    not st.session_state.access_token
    and "code" in st.query_params
):

    result = supabase_client.exchange_code_for_session(
        st.query_params["code"]
    )

    st.query_params.clear()

    if "error" in result:

        st.session_state.auth_error = (
            f"Google sign-in failed: {result['error']}"
        )

        st.session_state.current_view = "login"

    else:

        st.session_state.access_token = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id = result["user_id"]
        st.session_state.user_email = result["email"]

        st.session_state.current_view = "dashboard"

        st.rerun()


# ============================================================
# AUTH HELPERS
# ============================================================

def is_authenticated():

    return bool(
        st.session_state.get("access_token")
    )


def logout():

    try:

        supabase_client.sign_out()

    except Exception:

        pass


    for key in (
        "access_token",
        "refresh_token",
        "user_id",
        "user_email",
    ):

        st.session_state[key] = None


    st.session_state.current_view = "landing"
    st.session_state.auth_error = None
    st.session_state.auth_info = None

    st.rerun()


# ============================================================
# NAVIGATION
# ============================================================

def navigate(view):

    st.session_state.current_view = view
    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():

    with st.sidebar:

        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        st.html(
            """
            <div class="sidebar-brand">

                <div class="brand-icon">
                    ✦
                </div>

                <div>

                    <div class="brand-name">
                        HireMind AI
                    </div>

                    <div class="brand-subtitle">
                        Resume Intelligence
                    </div>

                </div>

            </div>
            """
        )


        st.html(
            """
            <div class="sidebar-divider"></div>
            """
        )


        # ----------------------------------------------------
        # WORKSPACE
        # ----------------------------------------------------

        st.html(
            """
            <div class="sidebar-section-title">
                WORKSPACE
            </div>
            """
        )


        if st.button(
            "⌂  Dashboard",
            key="nav_dashboard",
            use_container_width=True,
        ):

            navigate("dashboard")


        if st.button(
            "✦  Analyze Resume",
            key="nav_scorer",
            use_container_width=True,
        ):

            navigate("scorer")


        if st.button(
            "◷  Analysis History",
            key="nav_history",
            use_container_width=True,
        ):

            navigate("history")


        # ----------------------------------------------------
        # LEARN
        # ----------------------------------------------------

        st.html(
            """
            <div class="sidebar-section-title">
                LEARN
            </div>
            """
        )


        if st.button(
            "▣  Resources",
            key="nav_resources",
            use_container_width=True,
        ):

            navigate("resources")


        # ----------------------------------------------------
        # ACCOUNT
        # ----------------------------------------------------

        st.html(
            """
            <div class="sidebar-section-title">
                ACCOUNT
            </div>
            """
        )


        user_email = st.session_state.get(
            "user_email"
        )


        avatar_letter = (
            (user_email or "U")[0].upper()
        )


        st.html(
            f"""
            <div class="sidebar-user">

                <div class="sidebar-user-avatar">
                    {avatar_letter}
                </div>

                <div class="sidebar-user-info">

                    <div class="sidebar-user-label">
                        Signed in as
                    </div>

                    <div class="sidebar-user-email">
                        {user_email or "User"}
                    </div>

                </div>

            </div>
            """
        )


        if st.button(
            "↪  Sign out",
            key="nav_logout",
            use_container_width=True,
        ):

            logout()


# ============================================================
# AUTHENTICATED VIEW ROUTER
# ============================================================

def render_authenticated_view():

    render_sidebar()

    current_view = (
        st.session_state.current_view
    )


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    if current_view == "dashboard":

        from frontend.views import home

        home.render()


    # --------------------------------------------------------
    # RESUME ANALYZER
    # --------------------------------------------------------

    elif current_view == "scorer":

        from frontend.views import scorer

        scorer.render()


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    elif current_view == "history":

        from frontend.views import history

        history.render()


    # --------------------------------------------------------
    # RESOURCES
    # --------------------------------------------------------

    elif current_view == "resources":

        from frontend.views import resources

        resources.render()


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    else:

        st.session_state.current_view = "dashboard"

        st.rerun()


# ============================================================
# PUBLIC VIEW ROUTER
# ============================================================

def render_public_view():

    current_view = (
        st.session_state.current_view
    )


    # --------------------------------------------------------
    # LANDING
    # --------------------------------------------------------

    if current_view == "landing":

        from frontend.views import landing

        landing.render()


    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    elif current_view == "login":

        from frontend.views import login

        login.render()


    # --------------------------------------------------------
    # SIGNUP
    # --------------------------------------------------------

    elif current_view == "signup":

        from frontend.views import signup

        signup.render()


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    else:

        st.session_state.current_view = "landing"

        st.rerun()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if is_authenticated():

    render_authenticated_view()

else:

    render_public_view()