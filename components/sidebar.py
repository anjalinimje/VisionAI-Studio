import streamlit as st
from pathlib import Path
import base64
import html

PAGES = [
    "Image Detection",
    "Video Detection",
    "Webcam Detection",
    "Dashboard",
    "History",
    "Reports",
    "Settings",
    "About",
]

MODELS = [
    "YOLOv8n",
    "YOLOv8s",
    "YOLOv8m",
    "YOLOv8l",
    "YOLOv8x",
    "YOLO11n",
    "YOLO11s",
    "YOLO11m",
    "YOLO11l",
    "YOLO11x",
]

# Display ratings used by the current VisionAI Studio sidebar.
# These are relative UI ratings, not measured benchmark scores.
MODEL_INFO = {
    "YOLOv8n": ("Fastest Model", 4, 5),
    "YOLOv8s": ("Balanced Model", 4, 4),
    "YOLOv8m": ("Balanced Model", 5, 4),
    "YOLOv8l": ("High Accuracy", 5, 3),
    "YOLOv8x": ("Maximum Accuracy", 5, 2),
    "YOLO11n": ("Fastest Model", 4, 5),
    "YOLO11s": ("Balanced Model", 4, 4),
    "YOLO11m": ("Balanced Model", 5, 4),
    "YOLO11l": ("High Accuracy", 5, 3),
    "YOLO11x": ("Maximum Accuracy", 5, 2),
}


def load_svg(svg_path):
    """Load an SVG as a data URI if another part of the app needs it."""
    svg = Path(svg_path).read_text(encoding="utf-8")
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"


def _render_model_card(model):
    """Render the compact neon-styled model card inside the Streamlit sidebar."""
    desc, accuracy, speed = MODEL_INFO.get(
        model, ("Balanced Model", 4, 4)
    )
    safe_model = html.escape(model)

    st.markdown(
        """
        <style>
        .vision-model-card {
            box-sizing: border-box;
            width: 100%;
            margin: 5px 0 6px;
            padding: 4px 8px 9px;
            border: 1px solid rgba(168, 85, 247, .62);
            border-radius: 16px;
            background:
                radial-gradient(ellipse at 100% 0%, rgba(139, 92, 246, .22), transparent 48%),
                linear-gradient(145deg, rgba(22, 15, 47, .98), rgba(8, 11, 27, .99));
            box-shadow: 0 0 0 1px rgba(139, 92, 246, .08),
                        0 0 18px rgba(124, 58, 237, .13),
                        inset 0 1px 0 rgba(216, 180, 254, .09);
            color: #edf3ff;
            font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .vision-model-card .model-eyebrow {
            color: #c4b5fd;
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .vision-model-card .model-name {
            color: #faf5ff;
            text-shadow: 0 0 14px rgba(168, 85, 247, .22);
            font-size: 21px;
            font-weight: 750;
            line-height: 1.2;
            letter-spacing: -.35px;
            margin-bottom: 5px;
            overflow-wrap: anywhere;
        }
        .vision-model-card .model-badge {
            display: inline-block;
            padding: 4px 9px;
            border-radius: 999px;
            color: #e9d5ff;
            background: linear-gradient(90deg, rgba(124, 58, 237, .28), rgba(79, 70, 229, .16));
            border: 1px solid rgba(167, 139, 250, .30);
            font-size: 10px;
            line-height: 1.3;
            margin-bottom: 9px;
        }
        .vision-model-card .metric-label {
            color: #c4b5fd;
            font-size: 11px;
            margin: 0 0 4px;
        }
        .vision-model-card .rating-stars {
            color: #FFD34E;
            font-size: 18px;
            letter-spacing: 1px;
            line-height: 1.15;
            margin-bottom: 7px;
            text-shadow: 0 0 8px rgba(255, 211, 78, .38);
            white-space: nowrap;
        }
        .vision-model-card .rating-stars .empty {
            color: #4b4567;
            text-shadow: none;
        }
        .vision-model-card .classes-value {
            color: #e9d5ff;
            font-size: 12px;
            margin-top: 1px;
        }
        /* Purple accents for Streamlit sidebar controls */
        section[data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(105deg, #7c3aed 0%, #5b21b6 100%);
            border: 1px solid rgba(192, 132, 252, .65);
            color: #ffffff;
            box-shadow: 0 0 14px rgba(139, 92, 246, .24);
        }
        section[data-testid="stSidebar"] button[kind="secondary"] {
            background: rgba(22, 15, 47, .62);
            border: 1px solid rgba(139, 92, 246, .20);
            color: #e9d5ff;
        }
        section[data-testid="stSidebar"] button[kind="secondary"]:hover {
            border-color: rgba(192, 132, 252, .72);
            color: #ffffff;
            background: rgba(91, 33, 182, .24);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    accuracy_stars = "★" * accuracy + '<span class="empty">' + "☆" * (5 - accuracy) + "</span>"
    speed_stars = "★" * speed + '<span class="empty">' + "☆" * (5 - speed) + "</span>"

    st.markdown(
        f"""
        <div class="vision-model-card"><div class="model-eyebrow">Model in Use</div><div class="model-name">{safe_model}</div><div class="model-badge">{html.escape(desc)}</div><div class="metric-label">Accuracy</div><div class="rating-stars">{accuracy_stars}</div><div class="metric-label">Speed</div><div class="rating-stars">{speed_stars}</div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    # ---------- Session State ----------
    if "page" not in st.session_state:
        st.session_state.page = "Image Detection"

    if "model" not in st.session_state:
        st.session_state.model = "YOLOv8m"

    if "confidence" not in st.session_state:
        st.session_state.confidence = 0.25

    if "change_model" not in st.session_state:
        st.session_state.change_model = False

    # ---------- Logo ----------
    # Preserve the existing VisionAI Studio logo assets if available.
    logo_path = Path("assets/vision_eye.svg")
    if logo_path.exists():
        try:
            logo_uri = load_svg(logo_path)
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:10px;margin:2px 0 20px;">
                    <img src="{logo_uri}" style="width:42px;height:42px;object-fit:contain;">
                    <div>
                        <div style="font-size:23px;font-weight:800;line-height:1.05;color:#f3f6ff;">VisionAI</div>
                        <div style="font-size:20px;font-weight:750;line-height:1.15;color:#8b5cf6;">Studio</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except (OSError, ValueError):
            st.markdown("## VisionAI\n### Studio")
    else:
        st.markdown("## VisionAI\n### Studio")

    # ---------- Navigation ----------
    icons = {
        "Image Detection": "▧",
        "Video Detection": "▷",
        "Webcam Detection": "◎",
        "Dashboard": "▥",
        "History": "◷",
        "Reports": "▤",
        "Settings": "⚙",
        "About": "ⓘ",
    }

    for page in PAGES:
        if st.button(
            f"{icons[page]}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if st.session_state.page == page else "secondary",
        ):
            st.session_state.page = page

    st.divider()

    # ---------- Change Model control (above the card) ----------
    if st.button("⚙  Change Model", key="toggle_change_model", use_container_width=True):
        st.session_state.change_model = not st.session_state.change_model

    # Show the model controls immediately below the button when expanded.
    if st.session_state.change_model:
        st.selectbox("YOLO Model", MODELS, key="model")
        st.slider("Confidence", 0.0, 1.0, key="confidence", step=0.05)

        if st.button("Apply", key="apply_model", use_container_width=True):
            st.session_state.change_model = False
            st.rerun()

    # ---------- Model card ----------
    _render_model_card(st.session_state.model)

    return (
        st.session_state.page,
        st.session_state.model,
        st.session_state.confidence,
    )
