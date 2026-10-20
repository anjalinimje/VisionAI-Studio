import streamlit as st
import tempfile
import os
import cv2
from pathlib import Path
from analytics import object_bar_chart, object_pie_chart, confidence_histogram, confidence_gauge
from detector import Detector
from components.cards import info_card, ai_summary_card
from utils import generate_ai_summary
from modules.dashboard import save_detection_summary, save_detection_preview

def _video_detection_styles():
    """Neon blue-purple styling scoped to the video detection page/upload widget."""
    st.markdown(
        """
        <style>
        :root {
            --video-neon: #8275ff;
            --video-neon-bright: #a78bfa;
            --video-cyan: #35cfff;
            --video-panel: rgba(13, 17, 43, 0.78);
            --video-border: rgba(130, 117, 255, 0.68);
        }

        /* Page title and section headings */
        .stApp h1, .stApp h2, .stApp h3 {
            text-shadow: 0 0 14px rgba(130, 117, 255, 0.16);
        }

        /* One unified glossy panel around the title, subtitle and uploader. */
        .st-key-video_detection_panel {
            position: relative;
            padding: 22px 24px 20px;
            margin: 14px 0 24px;
            border: 1px solid rgba(130, 117, 255, 0.62);
            border-radius: 18px;
            background: linear-gradient(135deg,
                rgba(29, 25, 72, 0.55),
                rgba(8, 15, 37, 0.76) 58%,
                rgba(36, 20, 73, 0.42));
            box-shadow: inset 0 0 18px rgba(130, 117, 255, 0.045),
                        0 0 10px rgba(130, 117, 255, 0.09);
            overflow: hidden;
        }
        .st-key-video_detection_panel::before {
            content: "";
            position: absolute;
            top: 0;
            left: 22px;
            right: 22px;
            height: 1px;
            background: linear-gradient(90deg, transparent, #8b7bff, #43d9ff, transparent);
            opacity: .7;
            pointer-events: none;
        }
        /* Remove the uploader's extra outer card; retain only its dashed drop area. */
        .st-key-video_detection_panel .st-key-video_upload {
            padding: 0 !important;
            margin: 14px 0 0 !important;
            border: 0 !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            overflow: visible !important;
        }
        .st-key-video_detection_panel .st-key-video_upload::before {
            display: none !important;
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploader"] {
            border: 1px dashed rgba(157, 145, 255, 0.72);
            border-radius: 12px;
            background: rgba(7, 11, 29, 0.28);
            padding: 10px 13px;
            transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploader"]:hover {
            border-color: #a99cff;
            background: rgba(37, 28, 82, 0.28);
            box-shadow: 0 0 9px rgba(130, 117, 255, 0.14);
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploaderDropzone"] {
            background: transparent;
            border: 0;
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploaderDropzone"] button {
            color: #fff !important;
            border: 1px solid rgba(139, 123, 255, .85) !important;
            border-radius: 9px !important;
            background: linear-gradient(135deg, #5d35e8, #792cff) !important;
            box-shadow: 0 0 10px rgba(121, 44, 255, .20);
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploaderDropzone"] button:hover {
            border-color: #b7aaff !important;
            box-shadow: 0 0 14px rgba(130, 117, 255, .30);
        }
        .st-key-video_detection_panel .st-key-video_upload [data-testid="stFileUploaderDropzoneInstructions"] {
            color: #d8dcff;
        }

        /* Progress bar: dark track + restrained neon blue/purple fill */
        .stApp [data-testid="stProgressBar"] {
            padding: 5px 0;
        }
        .stApp [data-testid="stProgressBar"] > div {
            height: 8px !important;
            border-radius: 999px !important;
            overflow: hidden !important;
            background: rgba(130, 117, 255, 0.16) !important;
            border: 1px solid rgba(130, 117, 255, 0.25) !important;
        }
        .stApp [data-testid="stProgressBar"] > div > div {
            height: 100% !important;
            border-radius: 999px !important;
            background: linear-gradient(90deg, #28c7ff 0%, #6675ff 48%, #a855f7 100%) !important;
            box-shadow: 0 0 8px rgba(139, 92, 246, 0.28) !important;
        }

        /* Processing messages and completion notices match the glass UI */
        .stApp [data-testid="stAlert"] {
            border: 1px solid rgba(130, 117, 255, 0.48) !important;
            border-radius: 12px !important;
            background: linear-gradient(120deg, rgba(30, 32, 78, 0.82), rgba(11, 18, 42, 0.88)) !important;
            color: #e8eaff !important;
            box-shadow: 0 0 10px rgba(130, 117, 255, 0.08) !important;
        }
        .stApp [data-testid="stAlert"] p,
        .stApp [data-testid="stAlert"] span {
            color: #e8eaff !important;
        }
        .stApp [data-testid="stSpinner"] > div {
            color: #d9d5ff !important;
        }
        .stApp [data-testid="stSpinner"] svg {
            stroke: #9b8aff !important;
        }

        /* Uploaded filename row: blend it into the same dark glass panel */
        .st-key-video_detection_panel [data-testid="stFileUploaderFile"] {
            border: 1px solid rgba(130, 117, 255, 0.34) !important;
            border-radius: 10px !important;
            background: rgba(17, 22, 51, 0.66) !important;
            color: #e8eaff !important;
        }
        .st-key-video_detection_panel [data-testid="stFileUploaderFile"] p,
        .st-key-video_detection_panel [data-testid="stFileUploaderFile"] span {
            color: #dfe2ff !important;
        }
        .st-key-video_detection_panel [data-testid="stFileUploaderFile"] button {
            color: #f3efff !important;
            border: 1px solid rgba(151, 124, 255, 0.72) !important;
            border-radius: 8px !important;
            background: rgba(105, 60, 225, 0.76) !important;
        }
        .st-key-video_detection_panel [data-testid="stFileUploaderFile"] button:hover {
            background: rgba(126, 76, 255, 0.92) !important;
            box-shadow: 0 0 10px rgba(130, 117, 255, 0.22) !important;
        }


        /* Gradient section titles: consistent with VisionAI Studio's cyan/purple identity */
        .video-section-heading {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 26px 0 14px;
            color: #f5f3ff;
            font-size: 1.55rem;
            line-height: 1.25;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        .video-section-heading .video-heading-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            flex: 0 0 36px;
            border: 1px solid rgba(139, 123, 255, .62);
            border-radius: 11px;
            color: #c6baff;
            background: linear-gradient(135deg, rgba(47, 194, 255, .13), rgba(133, 63, 255, .24));
            box-shadow: inset 0 0 12px rgba(130, 117, 255, .07), 0 0 9px rgba(130, 117, 255, .10);
            font-size: 1.1rem;
        }
        .video-section-heading .video-heading-text {
            background: linear-gradient(90deg, #39d5ff 0%, #8275ff 52%, #c45bff 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        /* Loading/completed status: glossy purple glass, never the default green alert */
        .video-status-card {
            display: flex;
            align-items: center;
            gap: 11px;
            width: fit-content;
            max-width: 100%;
            margin: 12px 0 16px;
            padding: 13px 17px;
            border: 1px solid rgba(139, 123, 255, .58);
            border-radius: 13px;
            color: #eeeaff;
            background: linear-gradient(120deg, rgba(35, 30, 82, .88), rgba(11, 19, 44, .92) 62%, rgba(54, 25, 88, .72));
            box-shadow: inset 0 0 16px rgba(139, 123, 255, .06), 0 0 13px rgba(130, 117, 255, .12);
            font-weight: 650;
        }
        .video-status-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            flex: 0 0 28px;
            border-radius: 9px;
            color: #c6baff;
            border: 1px solid rgba(139, 123, 255, .45);
            background: rgba(114, 77, 255, .18);
        }
        .video-status-card.complete .video-status-icon {
            color: #5ce4ff;
            border-color: rgba(67, 217, 255, .42);
            background: rgba(67, 217, 255, .10);
        }
        .video-status-card .status-detail {
            display: block;
            margin-top: 3px;
            color: #b9c2e8;
            font-size: .84rem;
            font-weight: 450;
        }

        /* Keep the status slot from inheriting Streamlit's default alert styling */
        .stApp [data-testid="stAlert"] {
            border-color: rgba(139, 123, 255, .48) !important;
            background: linear-gradient(120deg, rgba(30, 32, 78, .82), rgba(11, 18, 42, .88)) !important;
            color: #e8eaff !important;
        }

        /* Polished action buttons */
        .stApp [data-testid="stDownloadButton"] button {
            color: #fff !important;
            border: 1px solid rgba(139, 123, 255, .85) !important;
            border-radius: 10px !important;
            background: linear-gradient(135deg, #5633d8, #7c2dff) !important;
            box-shadow: 0 0 12px rgba(124, 45, 255, .18);
        }
        .stApp [data-testid="stDownloadButton"] button:hover {
            border-color: #b6a8ff !important;
            box-shadow: 0 0 16px rgba(130, 117, 255, .32);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def _video_section_heading(icon, title):
    st.markdown(
        f'''
        <div class="video-section-heading">
            <span class="video-heading-icon">{icon}</span>
            <span class="video-heading-text">{title}</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )


def show_video_page(model_name, confidence):
    _video_detection_styles()

    # Keep the heading, helper text and uploader together in one glossy panel,
    # matching the Image Detection card. The Streamlit sidebar is untouched.
    with st.container(key="video_detection_panel"):
        st.markdown(
            """
            <div style="margin:0 0 2px 0;">
              <div style="font-size:1.85rem;font-weight:800;line-height:1.2;">
                <span style="display:inline-flex;align-items:center;gap:10px;">
                  <span style="display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;border:1px solid rgba(130,117,255,.62);background:linear-gradient(135deg,rgba(64,70,180,.35),rgba(96,35,170,.35));box-shadow:0 0 10px rgba(130,117,255,.14);font-size:1.25rem;">▶</span>
                  <span><span style="color:#42cfff;">Video</span> <span style="background:linear-gradient(90deg,#8275ff,#c15cff);-webkit-background-clip:text;background-clip:text;color:transparent;">Detection</span></span>
                </span>
              </div>
              <div style="color:#c7cce6;margin-top:7px;">Analyze video frames with your selected YOLO model and explore detection insights.</div>
            </div>
            <div style="font-weight:700;color:#b6a8ff;font-size:1rem;margin-top:16px;margin-bottom:-8px;">📁 Upload a video</div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_video = st.file_uploader(
            "Choose a video file",
            type=["mp4", "avi", "mov", "mkv"],
            key="video_upload",
            help="Supported formats: MP4, AVI, MOV, and MKV.",
            label_visibility="visible",
        )

    if uploaded_video is None:
        # Deliberately no st.info card here: the unified upload panel is the empty state.
        return

    # Save the uploaded video to a temporary file for the detector.
    suffix = Path(uploaded_video.name).suffix or ".mp4"
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_input.write(uploaded_video.getvalue())
    temp_input.close()

    os.makedirs("outputs", exist_ok=True)
    output_video = os.path.join("outputs", "detected_video.mp4")

    detector = Detector(f"models/{model_name.lower()}.pt", confidence)
    progress = st.progress(0)
    status = st.empty()

    try:
        with st.spinner("✨ Processing video frames..."):
            status.markdown(
                """
                <div class="video-status-card">
                    <span class="video-status-icon">✦</span>
                    <span>Loading the selected YOLO model
                        <span class="status-detail">Preparing the model for video analysis…</span>
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            progress.progress(20)
            video_summary = detector.detect_video(temp_input.name, output_video)
            object_counts = video_summary["object_counts"]
            object_confidences = video_summary["object_confidences"]
            confidence_scores = video_summary["confidence_scores"]
            total_objects = video_summary["total_objects"]
            total_classes = video_summary["unique_classes"]
            total_frames = video_summary["total_frames"]
            progress.progress(100)
            status.markdown(
                """
                <div class="video-status-card complete">
                    <span class="video-status-icon">✓</span>
                    <span>Video analysis complete
                        <span class="status-detail">Frames processed and detection results are ready.</span>
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        save_detection_summary(
            source="Video",
            object_counts=object_counts,
            confidence_scores=confidence_scores,
            total_objects=total_objects,
            model_name=model_name,
        )
        summary = generate_ai_summary(object_counts, confidence_scores, model_name)

        # Save representative original and annotated frames for the Dashboard.
        original_frame = None
        detected_frame = None
        for video_path, target in ((temp_input.name, "original"), (output_video, "detected")):
            capture = cv2.VideoCapture(video_path)
            last_frame = None
            if capture.isOpened():
                while True:
                    ok, frame = capture.read()
                    if not ok:
                        break
                    last_frame = frame
            capture.release()
            if last_frame is not None:
                import cv2 as _cv2
                rgb_frame = _cv2.cvtColor(last_frame, _cv2.COLOR_BGR2RGB)
                if target == "original":
                    original_frame = rgb_frame
                else:
                    detected_frame = rgb_frame

        save_detection_preview(
            source="Video",
            original_image=original_frame,
            detected_image=detected_frame,
            object_counts=object_counts,
            confidence_scores=confidence_scores,
            model_name=model_name,
            scene_summary=summary,
        )

        if total_objects == 0:
            st.warning("No objects were detected in this video. Try a different clip or model.")
            ai_summary_card(summary)
            return

        _video_section_heading("▶", "Video Preview")
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("**Original video**")
            st.video(temp_input.name)
        with right:
            st.markdown("**✨ Detected video**")
            st.video(output_video)

        st.divider()
        _video_section_heading("◎", "Detection Summary")
        c1, c2, c3, c4 = st.columns(4, gap="medium")
        with c1:
            info_card("🎯", "Objects", total_objects, "Objects detected")
        with c2:
            info_card("🧩", "Classes", total_classes, "Unique object classes")
        with c3:
            info_card("🧠", "Model", model_name, "YOLO model used")
        with c4:
            info_card("🎞️", "Frames", total_frames, "Frames processed")

        st.divider()
        _video_section_heading("⌁", "Detection Analytics")
        st.caption("Analytics are calculated across the processed video frames.")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            object_bar_chart(object_counts)
        with col2:
            object_pie_chart(object_counts)

        col3, col4 = st.columns(2, gap="large")
        with col3:
            histogram_fig = confidence_histogram(confidence_scores)
            st.plotly_chart(histogram_fig, use_container_width=True)
        with col4:
            gauge_fig = confidence_gauge(confidence_scores)
            st.plotly_chart(gauge_fig, use_container_width=True)

        st.divider()
        _video_section_heading("✧", "AI Detection Summary")
        ai_summary_card(summary)

        st.divider()
        _video_section_heading("↓", "Export")
        with open(output_video, "rb") as video_file:
            st.download_button(
                label="⬇️  Download detected video",
                data=video_file,
                file_name="detected_video.mp4",
                mime="video/mp4",
                use_container_width=False,
            )
        st.caption("VisionAI Studio · Video analysis")
    finally:
        # Temporary input is no longer needed after processing/playback is rendered.
        # Keep it until this run finishes; then remove it to avoid accumulating temp files.
        try:
            os.unlink(temp_input.name)
        except OSError:
            pass
