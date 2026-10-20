

import cv2
import streamlit as st
import pandas as pd
from detector import Detector
import io
from components.cards import info_card, ai_summary_card, detection_cards    
from PIL import Image
from analytics import confidence_histogram, object_bar_chart, object_pie_chart, confidence_gauge
from utils import generate_ai_summary
from modules.dashboard import save_detection_summary
from modules.dashboard import save_detection_preview


def _neon_section(title, icon="sparkles"):
    """Render a section title that matches VisionAI Studio's neon-purple theme."""
    icons = {
        "image": '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="1.5"/><path d="m4 17 5-5 4 4 3-3 4 4"/>',
        "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
        "summary": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
        "analytics": '<path d="M3 3v18h18"/><path d="m7 14 4-4 3 3 6-7"/>',
        "brain": '<path d="M12 4a4 4 0 0 0-7 3 4 4 0 0 0-1 7 4 4 0 0 0 4 6h4z"/><path d="M12 4a4 4 0 0 1 7 3 4 4 0 0 1 1 7 4 4 0 0 1-4 6h-4z"/><path d="M8 9c2 0 2 2 2 3m-3 3c2-1 3 0 3 2m5-8c-2 0-2 2-2 3m3 3c-2-1-3 0-3 2"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
        "download": '<path d="M12 3v12m-5-5 5 5 5-5"/><path d="M4 17v3h16v-3"/>',
    }
    shape = icons.get(icon, icons["summary"])
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin:20px 0 14px 0;">
          <span style="display:flex;align-items:center;justify-content:center;
            width:34px;height:34px;flex:0 0 34px;border-radius:10px;
            background:linear-gradient(135deg,rgba(56,207,255,.12),rgba(139,92,246,.22));
            border:1px solid rgba(167,139,250,.48);
            box-shadow:0 0 16px rgba(139,92,246,.16);">
            <svg width="21" height="21" viewBox="0 0 24 24" fill="none"
              stroke="#C4B5FD" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">{shape}</svg>
          </span>
          <span style="font-size:25px;font-weight:750;line-height:1.2;
            background:linear-gradient(90deg,#E9D5FF 0%,#A78BFA 55%,#38CFFF 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;">{title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_image_page(model_name, confidence):
    
    
    st.markdown(
        """
        <style>
        /* Streamlit may put the user key on the container itself OR on a wrapper.
           Style both, so the outer panel always gets the neon edge. */
        .st-key-image_detection_panel,
        .st-key-image_detection_panel [data-testid="stVerticalBlockBorderWrapper"] {
            position: relative !important;
            overflow: visible !important;
            border: 1px solid #A855F7 !important;
            border-radius: 16px !important;
            background:
                radial-gradient(ellipse at 12% 0%, rgba(168, 85, 247, 0.22), transparent 48%),
                linear-gradient(145deg, rgba(28, 18, 59, 0.98) 0%, rgba(12, 13, 34, 0.99) 58%, rgba(25, 14, 52, 0.98) 100%) !important;
            box-shadow:
                0 0 0 1px rgba(192, 132, 252, 0.22),
                0 0 6px rgba(192, 132, 252, 0.95),
                0 0 14px rgba(168, 85, 247, 0.78),
                0 0 28px rgba(124, 58, 237, 0.52),
                inset 0 1px 0 rgba(255, 255, 255, 0.18),
                inset 0 0 18px rgba(139, 92, 246, 0.14) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* Subtle glossy neon-purple Image Detection card */
.st-key-image_detection_panel,
.st-key-image_detection_panel [data-testid="stVerticalBlockBorderWrapper"] {
    position: relative !important;
    border: 1px solid rgba(167, 139, 250, 0.58) !important;
    border-radius: 15px !important;

    background:
        radial-gradient(
            ellipse at 12% 0%,
            rgba(139, 92, 246, 0.10),
            transparent 55%
        ),
        linear-gradient(
            145deg,
            rgba(25, 18, 48, 0.97),
            rgba(10, 13, 31, 0.98)
        ) !important;

    /* Thin border and restrained glow */
    box-shadow:
        0 0 3px rgba(168, 85, 247, 0.28),
        0 0 9px rgba(124, 58, 237, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.07),
        inset 0 0 10px rgba(139, 92, 246, 0.04) !important;

    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

/* Soft glossy line along the top */
.st-key-image_detection_panel::before,
.st-key-image_detection_panel
[data-testid="stVerticalBlockBorderWrapper"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 10%;
    right: 10%;
    height: 1px;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(216, 180, 254, 0.48),
        rgba(255, 255, 255, 0.38),
        rgba(216, 180, 254, 0.48),
        transparent
    );

    box-shadow: 0 0 4px rgba(168, 85, 247, 0.28);
    pointer-events: none;
    z-index: 3;
}

/* Keep the content spacing compact */
.st-key-image_detection_panel
[data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

/* Remove the uploader's extra outer box */
.st-key-image_detection_panel
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    border-radius: 0 !important;
}

/* Keep the upload drop zone's subtle dashed border */
.st-key-image_detection_panel
[data-testid="stFileUploaderDropzone"] {
    background: rgba(11, 15, 35, 0.35) !important;
    border: 1px dashed rgba(167, 139, 250, 0.55) !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

.st-key-image_detection_panel
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(192, 132, 252, 0.85) !important;
    box-shadow: 0 0 6px rgba(139, 92, 246, 0.16) !important;
}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True, key="image_detection_panel"):
        st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin:4px 0 3px 0;">
        <div style="
            width:42px;
            height:42px;
            flex:0 0 42px;
            display:flex;
            align-items:center;
            justify-content:center;
            margin:0;
            border-radius:12px;
            background:rgba(139,92,246,0.15);
            border:1px solid rgba(139,92,246,0.45);
            box-shadow:0 0 16px rgba(139,92,246,0.18);
        ">
            <svg width="30" height="30" viewBox="0 0 48 48"
                 xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="scanIcon" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0%" stop-color="#38CFFF"/>
                        <stop offset="55%" stop-color="#8B5CF6"/>
                        <stop offset="100%" stop-color="#D946EF"/>
                    </linearGradient>
                </defs>
                <path d="M14 7H9Q4 7 4 12V17 M34 7H39Q44 7 44 12V17
                         M4 31V36Q4 41 9 41H14 M34 41H39Q44 41 44 36V31"
                      fill="none" stroke="#A78BFA" stroke-width="2.5"
                      stroke-linecap="round"/>
                <rect x="10" y="13" width="28" height="23" rx="4"
                      fill="none" stroke="url(#scanIcon)" stroke-width="2.4"/>
                <circle cx="19" cy="21" r="3"
                        fill="none" stroke="url(#scanIcon)" stroke-width="2"/>
                <path d="M13 32L21 25L27 30L32 24L35 29"
                      fill="none" stroke="url(#scanIcon)" stroke-width="2.2"
                      stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
    

    <span style="
        display:block;
        line-height:1.2;
        margin:0;
        padding:0;
        font-size:35px;
        font-weight:700;
        background:linear-gradient(90deg,#38CFFF 0%,#8B5CF6 65%,#D946EF 100%);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        background-clip:text;
    ">
        Image Detection
    
    </span>


    </div>
    """, unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                margin:0 0 7px 45px;
                padding:0;
                color:#C7D2FE;
                font-size:15px;
                line-height:1.4;
            ">Choose an image to detect objects in.</div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose an Image",
            type=["jpg", "jpeg", "png"],
            key="image_upload",
            label_visibility="collapsed",
        )

    if uploaded_file is None:
        return

    # -----------------------------
    # Object Detection
    # -----------------------------
    with st.spinner("🔍 Detecting objects..."):

        detector = Detector(
            f"models/{model_name.lower()}.pt",
            confidence
        )

        image, results = detector.detect(uploaded_file)

    boxes = results[0].boxes

    if len(boxes) == 0:
        st.warning("⚠️ No objects detected in this image.")

    total_objects = len(boxes)

    unique_classes = set()

    object_counts = {}

    detection_data = []

    confidence_scores = []

    object_confidences = {}
    
    for box in boxes:

        class_id = int(box.cls[0])

        class_name = detector.model.names[class_id]

        confidence_score = float(box.conf[0])

        confidence_scores.append(round(confidence_score, 2))

        unique_classes.add(class_name)

        object_counts[class_name] = object_counts.get(class_name, 0) + 1
        if class_name not in object_confidences:
            object_confidences[class_name] = []

        object_confidences[class_name].append(confidence_score)

        detection_data.append(
            {
                "Object": class_name,
                "Confidence": round(confidence_score, 2)
            }
        )

    total_classes = len(unique_classes)

    summary = generate_ai_summary(
                object_counts,
                confidence_scores,
                model_name
            )
    save_detection_summary(
        source="Image",
        object_counts=object_counts,
        confidence_scores=confidence_scores,
        total_objects=total_objects,
        model_name=model_name,
    )

    # Save the latest image and annotated result for the Dashboard.
    # Keep this before the zero-detections return so every scan has a preview.
    annotated = results[0].plot()
    save_detection_preview(
        source="Image",
        original_image=image,
        detected_image=annotated,
        object_counts=object_counts,
        confidence_scores=confidence_scores,
        model_name=model_name,
        scene_summary=summary,
    )

    if total_objects == 0:
        st.info("No objects detected, so analytics are unavailable.")

        _neon_section("AI Detection Summary", "brain")
        ai_summary_card(summary)

        return

    # -----------------------------
    # Images
    # -----------------------------
    left, right = st.columns(2)
        
    with left:
        
        _neon_section("Original Image", "image")
        
        st.image(image, use_container_width=True)
        
    with right:
        
        _neon_section("Detected Image", "target")
        
        st.image(annotated, use_container_width=True)
        
    st.divider()
    # -----------------------------
    # KPI Cards
    # -----------------------------
    _neon_section("Detection Summary", "summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        info_card(
            "📦",
            "Objects",
            total_objects,
            "Detected Objects"
        )

    with c2:

        info_card(
            "🎯",
            "Classes",
            total_classes,
            "Unique Classes"
        )

    with c3:

        info_card(
            "🤖",
            "Model",
            model_name,
            "YOLO Model"
        )

    with c4:

        status = "Success" if total_objects > 0 else "No Detection"
        subtitle = "Detection Complete" if total_objects > 0 else "No Objects Found"
        
        info_card(
            "✅" if total_objects > 0 else "⚠️",
            "Status",
            status,
            subtitle
        )

    st.divider()

    _neon_section("Detection Analytics", "analytics")
    
    col1, col2 = st.columns(2)

    with col1:
        object_bar_chart(object_counts)

    with col2:
        object_pie_chart(object_counts)


    st.divider()

    col3, col4 = st.columns(2)
    
    with col3:
        histogram_fig = confidence_histogram(confidence_scores)
        st.plotly_chart(histogram_fig, use_container_width=True)
    
    with col4:
        gauge_fig = confidence_gauge(confidence_scores)
        st.plotly_chart(gauge_fig, use_container_width=True)
    

    st.divider()



    _neon_section("AI Detection Summary", "brain")

    ai_summary_card(summary)

    st.divider()

    # =====================================================
    # Detection Explorer
    # =====================================================

    _neon_section("Detection Explorer", "search")

    st.caption(
        "Explore confidence scores and counts for each object detected in this image."
    )

    detection_cards(
        object_counts,
        object_confidences
    )

    st.divider()
    # -----------------------------
    # Download Image
    # -----------------------------
    _neon_section("Download Result", "download")

    detected_image = Image.fromarray(annotated)

    buffer = io.BytesIO()

    detected_image.save(buffer, format="JPEG")

    st.download_button(
        label="📥 Download Annotated Image",
        data=buffer.getvalue(),
        file_name="detected_image.jpg",
        mime="image/jpeg"
    )


