import streamlit as st

from streamlit_option_menu import option_menu

# UI
from components.sidebar import render_sidebar
from components.ui_components import load_css
from components.hero import hero


from modules.image_detection import show_image_page
from modules.video_detection import show_video_page
from modules.webcam_detection import show_webcam_page
from modules.dashboard import show_dashboard
from modules.about import show_about_page
from modules.settings import render_settings_page
from modules.history import show_history_page
from modules.reports import show_reports_page

##############################################################
# PAGE CONFIG
##############################################################

st.set_page_config(
    page_title="VisionAI Studio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

##############################################################
# LOAD CSS
##############################################################

load_css()

left, right = st.columns([1.15, 4.85], gap="medium")

##############################################################

##############################################################
# HERO
##############################################################

with left:
    selected, model_name, confidence = render_sidebar()

with right:

    hero()

    confidence = 0.25
    model_name = "YOLOv8m"


    if selected == "Image Detection":

        show_image_page(
            model_name=model_name,
            confidence=confidence
        )

    elif selected == "Video Detection":

        show_video_page(
            model_name=model_name,
            confidence=confidence
        )

    elif selected == "Webcam Detection":

        show_webcam_page(
            model_name=model_name,
            confidence=confidence
        )

    elif selected == "Dashboard":

        show_dashboard()

    elif selected == "About":
        show_about_page()

    elif selected == "Settings":
        render_settings_page()

    elif selected == "History":
        show_history_page()

    elif selected == "Reports":
        show_reports_page()
