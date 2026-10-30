import streamlit as st
from dotenv import load_dotenv
from database.db import init_db, create_user, verify_user
load_dotenv()
init_db()
st.set_page_config(
    page_title="Career Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--mint:#67e8c0;--navy:#08111f;--panel:#101d30;--muted:#a6b5c8}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 80% 0%,rgba(30,105,105,.18),transparent 40%),#08111f;color:#e8f0f7}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.03em}
[data-testid="stSidebar"]{background:#0b1627;border-right:1px solid #1c3045}
[data-testid="stSidebar"] *{color:#e8f0f7}
.stButton>button{border:1px solid #2c5c58;border-radius:10px;background:linear-gradient(120deg,#67e8c0,#39b99d);color:#06151a;font-weight:700;min-height:42px}
.stButton>button:hover{border-color:#8cf5d3;box-shadow:0 0 18px #39b99d44;color:#06151a}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]{background:#0d192a;color:#e8f0f7;border-color:#2a3d52;border-radius:9px}
[data-testid="stMetric"]{background:linear-gradient(145deg,#122238,#0d192a);border:1px solid #21374d;padding:16px;border-radius:14px}
[data-testid="stFileUploader"]{background:#0e1b2d;border:1px dashed #39665f;border-radius:14px;padding:12px}
div[data-testid="stExpander"]{border:1px solid #243a50;border-radius:12px}
small,.stCaption{color:#a6b5c8!important}
.hero{padding:24px 0 14px}.eyebrow{color:#67e8c0;text-transform:uppercase;letter-spacing:.16em;font-size:.78rem;font-weight:700}
.card{background:linear-gradient(145deg,#122238,#0d192a);border:1px solid #22384e;border-radius:16px;padding:20px;margin-bottom:12px}
.mint{color:#67e8c0}.muted{color:#a6b5c8}
/* Hide sidebar and arrow on login page */
body:has([data-testid="stForm"]) [data-testid="stSidebar"],
body:has([data-testid="stForm"]) [data-testid="stSidebarCollapsedControl"] {
    display: none !important;
</style>""",unsafe_allow_html=True)

if "user_id" not in st.session_state: st.session_state.user_id=None
if "username" not in st.session_state: st.session_state.username=None
if "auth_mode" not in st.session_state: st.session_state.auth_mode="Login"

if not st.session_state.user_id:
    left,center,right=st.columns([1,1.15,1])
    with center:
        st.markdown('<div class="hero"><div class="eyebrow">✦ Career intelligence platform</div><h1 style="font-size:2.5rem;margin-bottom:0">Find your next <span style="color:#67e8c0">career move.</span></h1><p style="color:#a6b5c8">Resume insights, explainable job matching and a skills roadmap.</p></div>',unsafe_allow_html=True)
        with st.container(border=True):
            st.segmented_control("Account",["Login","Create account"],key="auth_mode",default=st.session_state.auth_mode)
            mode=st.session_state.get("auth_mode","Login")
            with st.form("auth_form",clear_on_submit=False):
                username=st.text_input("Username",placeholder="Enter username",max_chars=60)
                password=st.text_input("Password",type="password",placeholder="At least 8 characters")
                submit=st.form_submit_button("Login securely" if mode=="Login" else "Create account",use_container_width=True)
            if submit:
                if mode=="Create account":
                    ok,msg=create_user(username,password); st.info(msg)
                else:
                    uid=verify_user(username,password) if username and password else None
                    if uid:
                        st.session_state.user_id=uid; st.session_state.username=username.strip(); st.rerun()
                    else: st.error("Login details तपासा. Username किंवा password चुकीचा आहे.")
        st.caption("Your analysis history is associated with your account. Do not upload documents you do not have permission to process.")
    st.stop()

# Show sidebar only after successful login
if st.session_state.get("user_id") is not None:

    with st.sidebar:
        st.markdown("## ✦ Career Intelligence")
        st.caption(f"Signed in as **{st.session_state.username}**")

        page = st.radio(
            "WORKSPACE",
            [
                "Overview",
                "Resume Analyzer",
                "Job Explorer",
                "Knowledge Graph",
                "Career Assistant",
                "Career Roadmap",
                "History"
            ],
            label_visibility="visible"
        )

        st.divider()

        if st.button("Log out", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

    # Display selected page only after login
    if page == "Overview":
        from pages.dashboard import render
        render()

    elif page == "Resume Analyzer":
        from pages.resume_analyzer import render
        render()

    elif page == "Job Explorer":
        from pages.job_explorer import render
        render()

    elif page == "Knowledge Graph":
        from pages.knowledge_graph import render
        render()

    elif page == "Career Assistant":
        from pages.career_assistant import render
        render()

    elif page == "Career Roadmap":
        from pages.roadmap_page import render
        render()

    elif page == "History":
        from pages.history import render
        render()
