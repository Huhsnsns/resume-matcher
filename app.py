"""ResumeMatch: landing page and dashboard. Run with: python -m streamlit run app.py"""

import streamlit as st

st.set_page_config(
    page_title="ResumeMatch · AI resume and job matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

import dashboard  # noqa: E402
import landing  # noqa: E402
import session  # noqa: E402
import styles  # noqa: E402

session.init_state()
styles.inject(st.session_state.page)

if st.session_state.page == "dashboard":
    dashboard.render()
else:
    landing.render()
