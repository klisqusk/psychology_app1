import streamlit as st


def setup_page():
    st.set_page_config(
        page_title="PsychoTest Pro",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def load_styles():
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
