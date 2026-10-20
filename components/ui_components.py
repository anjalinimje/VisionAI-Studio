import streamlit as st

from analytics import object_bar_chart

st.markdown("""
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
""", unsafe_allow_html=True)

def load_css():

    css = ""

    for file in [
        "assets/styles.css",
        "assets/hero.css",
        "assets/sidebar.css",
    ]:

        try:

            with open(file) as f:
                css += f.read()

        except FileNotFoundError:
            pass

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


