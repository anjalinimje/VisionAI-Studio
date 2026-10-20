import streamlit as st

"""VisionAI Studio settings page.

All card styles are scoped to this page's four explicitly keyed card buttons.
Sidebar navigation buttons are intentionally not styled here.
"""

ACCENT = "#9B5CFF"

DEFAULTS = {
    "settings_active_card": None,
    "settings_confidence": 0.25,
    "settings_show_boxes": True,
    "settings_show_labels": True,
    "settings_theme": "Neon Purple",
    "settings_glow": True,
    "settings_device": "Auto",
    "settings_processing": "Balanced",
    "settings_export_format": "PNG",
    "settings_include_summary": True,
    "settings_include_confidence": True,
}


def _initialise_settings():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _toggle_settings_card(card_key: str):
    current = st.session_state.get("settings_active_card")
    st.session_state["settings_active_card"] = None if current == card_key else card_key


def _reset_settings():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.session_state["settings_notice"] = "Settings reset to defaults."


def _render_settings_card(card_key: str, icon: str, title: str, subtitle: str):
    is_open = st.session_state.get("settings_active_card") == card_key
    action = "▾  Settings open" if is_open else "＋  Configure"
    st.button(
        f"{icon}  {title}\n\n{subtitle}\n\n{action}",
        key=f"settings_card_{card_key}",
        on_click=_toggle_settings_card,
        args=(card_key,),
        use_container_width=True,
        type="primary" if is_open else "secondary",
    )


def render_settings_page():
    _initialise_settings()

    # IMPORTANT: every button selector below is limited to the four settings
    # card keys. There are no global stButton or stHorizontalBlock overrides.
    st.markdown(
        """
        <style>
        .vision-settings-heading {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 17px 20px;
            margin: 0 0 18px 0;
            border: 1px solid rgba(155, 92, 255, .68);
            border-radius: 16px;
            background:
                radial-gradient(ellipse at 0% 0%, rgba(155,92,255,.17), transparent 65%),
                linear-gradient(145deg, rgba(23,18,51,.97), rgba(8,11,27,.98));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 0 10px rgba(155,92,255,.12);
        }
        .vision-settings-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 48px;
            width: 48px;
            height: 48px;
            border-radius: 13px;
            color: #E9D5FF;
            font-size: 23px;
            border: 1px solid rgba(168,85,247,.6);
            background: linear-gradient(145deg, rgba(139,92,246,.34), rgba(35,20,72,.75));
        }
        .vision-settings-title {
            color: #F8FAFC;
            font-size: 26px;
            line-height: 1.2;
            font-weight: 800;
            margin: 0;
        }
        .vision-settings-subtitle {
            color: #B7C0D8;
            font-size: 14px;
            margin-top: 5px;
        }

        /* The four card buttons only. Sidebar buttons are not matched. */
        div[class*="st-key-settings_card_detection"] button,
        div[class*="st-key-settings_card_appearance"] button,
        div[class*="st-key-settings_card_device"] button,
        div[class*="st-key-settings_card_export"] button {
            box-sizing: border-box !important;
            width: 100% !important;
            min-height: 132px !important;
            height: 132px !important;
            padding: 16px 18px !important;
            display: flex !important;
            align-items: flex-start !important;
            justify-content: flex-start !important;
            white-space: pre-wrap !important;
            text-align: left !important;
            line-height: 1.42 !important;
            color: #F3EEFF !important;
            background:
                radial-gradient(ellipse at 8% 0%, rgba(155,92,255,.18), transparent 72%),
                linear-gradient(145deg, rgba(24,19,54,.98), rgba(7,11,28,.99)) !important;
            border: 1px solid rgba(155,92,255,.72) !important;
            border-radius: 15px !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.045), 0 0 8px rgba(155,92,255,.13) !important;
            transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease !important;
        }
        div[class*="st-key-settings_card_detection"] button:hover,
        div[class*="st-key-settings_card_appearance"] button:hover,
        div[class*="st-key-settings_card_device"] button:hover,
        div[class*="st-key-settings_card_export"] button:hover {
            color: #FFFFFF !important;
            border-color: rgba(205,166,255,.98) !important;
            box-shadow: inset 0 0 12px rgba(155,92,255,.08), 0 0 15px rgba(155,92,255,.23) !important;
            transform: translateY(-2px);
        }
        div[class*="st-key-settings_card_detection"] button:focus,
        div[class*="st-key-settings_card_appearance"] button:focus,
        div[class*="st-key-settings_card_device"] button:focus,
        div[class*="st-key-settings_card_export"] button:focus {
            outline: 1px solid rgba(205,166,255,.8) !important;
            outline-offset: 2px !important;
        }
        div[class*="st-key-settings_card_detection"] button p,
        div[class*="st-key-settings_card_appearance"] button p,
        div[class*="st-key-settings_card_device"] button p,
        div[class*="st-key-settings_card_export"] button p {
            white-space: pre-wrap !important;
            text-align: left !important;
            line-height: 1.42 !important;
            margin: 0 !important;
        }

        .vision-settings-panel {
            border: 1px solid rgba(155,92,255,.60);
            border-radius: 15px;
            padding: 18px 20px 8px;
            margin: 16px 0 18px;
            background:
                radial-gradient(ellipse at 8% 0%, rgba(155,92,255,.12), transparent 70%),
                linear-gradient(145deg, rgba(21,17,48,.98), rgba(7,10,25,.99));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.035), 0 0 9px rgba(155,92,255,.12);
        }
        div[data-testid="stSlider"] label,
        div[data-testid="stCheckbox"] label,
        div[data-testid="stSelectbox"] label {
            color: #E9D5FF !important;
        }

        /* Save/reset actions are also scoped to their own keys. */
        div[class*="st-key-settings_reset_defaults"] button,
        div[class*="st-key-settings_save_preferences"] button {
            min-height: 42px !important;
            height: 42px !important;
            padding: 8px 14px !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: normal !important;
            text-align: center !important;
            border-radius: 10px !important;
        }
        @media (max-width: 700px) {
            .vision-settings-heading { padding: 14px; }
            .vision-settings-title { font-size: 23px; }
            div[class*="st-key-settings_card_detection"] button,
            div[class*="st-key-settings_card_appearance"] button,
            div[class*="st-key-settings_card_device"] button,
            div[class*="st-key-settings_card_export"] button {
                min-height: 118px !important;
                height: 118px !important;
                padding: 13px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="vision-settings-heading">
          <div class="vision-settings-icon">☷</div>
          <div>
            <div class="vision-settings-title">Settings</div>
            <div class="vision-settings-subtitle">Configure your VisionAI Studio experience.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Two rows of two cards. Each Streamlit button has a unique key and style.
    left, right = st.columns(2, gap="medium")
    with left:
        _render_settings_card("detection", "◎", "Detection Settings", "Model, confidence, labels")
    with right:
        _render_settings_card("appearance", "◉", "Appearance", "Theme, accents, effects")

    left, right = st.columns(2, gap="medium")
    with left:
        _render_settings_card("device", "◴", "Device & Processing", "Device and processing preferences")
    with right:
        _render_settings_card("export", "⇥", "Results & Export", "Output and save options")

    active = st.session_state.get("settings_active_card")
    if active:
        with st.container(key="settings_expanded_panel"):
            st.markdown('<div class="vision-settings-panel">', unsafe_allow_html=True)
            if active == "detection":
                st.markdown("### ◎ Detection Settings")
                st.caption("Configure confidence thresholds and detection overlays.")
                st.slider("Minimum confidence threshold", 0.05, 0.95, step=0.05, key="settings_confidence")
                st.checkbox("Show bounding boxes", key="settings_show_boxes")
                st.checkbox("Show object labels and confidence scores", key="settings_show_labels")
            elif active == "appearance":
                st.markdown("### ◉ Appearance")
                st.selectbox("Accent colour", ["Neon Purple", "Electric Blue", "Cyan", "Magenta"], key="settings_theme")
                st.checkbox("Enable interface glow effects", key="settings_glow")
            elif active == "device":
                st.markdown("### ◴ Device & Processing")
                st.selectbox("Inference device", ["Auto", "CPU", "CUDA GPU", "Apple Silicon (MPS)"], key="settings_device")
                st.selectbox("Processing profile", ["Fast", "Balanced", "High Accuracy"], key="settings_processing")
                st.caption("Available options depend on your hardware and model runtime.")
            elif active == "export":
                st.markdown("### ⇥ Results & Export")
                st.selectbox("Default export format", ["PNG", "CSV", "JSON"], key="settings_export_format")
                st.checkbox("Include detection summary when available", key="settings_include_summary")
                st.checkbox("Include confidence values in exported results", key="settings_include_confidence")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    reset_col, _, save_col = st.columns([1.3, 4, 1.4], gap="small")
    with reset_col:
        st.button("↺ Reset defaults", key="settings_reset_defaults", on_click=_reset_settings, use_container_width=True)
    with save_col:
        if st.button("Save settings", key="settings_save_preferences", type="primary", use_container_width=True):
            st.session_state["settings_notice"] = "Settings saved for this Streamlit session."

    notice = st.session_state.pop("settings_notice", None)
    if notice:
        st.success(notice)

    st.caption(
        "Preferences currently apply to this Streamlit session. "
        "Connect them to your model and global theme to apply them throughout the app."
    )


def show_settings_page():
    """Compatibility alias for apps importing show_settings_page."""
    render_settings_page()
