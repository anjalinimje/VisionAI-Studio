import csv
import html
import io
import time

import cv2
import streamlit as st

from components.cards import info_card, ai_summary_card, detection_cards
from detector import Detector
from analytics import (
    object_bar_chart,
    object_pie_chart,
    confidence_histogram,
    confidence_gauge,
)
from utils import generate_ai_summary
from modules.dashboard import save_detection_summary, save_detection_preview

WEBCAM_CSS = """
<style>
/* Webcam page palette: midnight glass + cyan/neon-purple accents */
.video-section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 25px 0 14px;
    color: #f5f3ff;
    font-size: 1.48rem;
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
    border: 1px solid rgba(139, 123, 255, .65);
    border-radius: 11px;
    color: #c9bdff;
    background: linear-gradient(135deg, rgba(44, 205, 255, .15), rgba(132, 55, 255, .28));
    box-shadow: inset 0 0 12px rgba(130, 117, 255, .08), 0 0 12px rgba(130, 117, 255, .12);
    font-size: 1.08rem;
}
.video-section-heading .video-heading-text {
    background: linear-gradient(90deg, #35d5ff 0%, #8175ff 52%, #cb63ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

/* One outlined glass panel for title, camera controls, live feed and live stats */
.st-key-webcam_detection_panel {
    border: 1px solid rgba(137, 111, 255, .82) !important;
    border-radius: 20px !important;
    padding: 22px 22px 18px !important;
    background:
        radial-gradient(ellipse at 10% 0%, rgba(79, 65, 190, .18), transparent 48%),
        linear-gradient(135deg, rgba(17, 21, 51, .84), rgba(7, 12, 31, .88) 60%, rgba(36, 17, 65, .72)) !important;
    box-shadow: inset 0 0 24px rgba(120, 98, 255, .07), 0 0 17px rgba(115, 83, 255, .13) !important;
    margin-bottom: 20px !important;
}
.st-key-webcam_detection_panel [data-testid="stImage"] img {
    border: 1px solid rgba(117, 111, 255, .68);
    border-radius: 14px;
    box-shadow: 0 0 18px rgba(92, 70, 255, .13);
}

/* LIVE / model / objects / FPS glossy metric tiles */
.webcam-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin: 15px 0 18px;
}
.webcam-stat-card {
    min-height: 90px;
    padding: 14px 13px 12px;
    border: 1px solid rgba(133, 116, 255, .67);
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(35, 36, 91, .80), rgba(13, 20, 48, .88) 62%, rgba(59, 27, 94, .65));
    box-shadow: inset 0 0 18px rgba(135, 110, 255, .06), 0 0 12px rgba(121, 91, 255, .10);
    text-align: center;
}
.webcam-stat-icon {
    font-size: 1.18rem;
    line-height: 1.3;
    color: #c5b6ff;
    text-shadow: 0 0 10px rgba(166, 125, 255, .6);
}
.webcam-stat-label {
    margin-top: 5px;
    color: #d9d6ff;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .035em;
    text-transform: uppercase;
}
.webcam-stat-value {
    margin-top: 5px;
    color: #41dcff;
    font-size: 1.08rem;
    font-weight: 850;
    overflow-wrap: anywhere;
}
.webcam-stat-detail {
    margin-top: 3px;
    color: #b9c3e7;
    font-size: .72rem;
}
@media (max-width: 700px) {
    .webcam-stat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .st-key-webcam_detection_panel { padding: 15px !important; }
}

/* Harmonize Streamlit buttons and alerts within this page */
.st-key-webcam_detection_panel .stButton > button {
    border: 1px solid rgba(148, 123, 255, .82) !important;
    border-radius: 11px !important;
    color: #f4f0ff !important;
    background: linear-gradient(110deg, rgba(43, 48, 130, .95), rgba(83, 31, 160, .95)) !important;
    box-shadow: 0 0 13px rgba(111, 79, 255, .18), inset 0 0 12px rgba(146, 125, 255, .09) !important;
    font-weight: 700 !important;
}
.st-key-webcam_detection_panel .stButton > button:hover {
    border-color: #43d9ff !important;
    box-shadow: 0 0 17px rgba(67, 217, 255, .22), 0 0 14px rgba(145, 92, 255, .2) !important;
}
.stApp [data-testid="stAlert"] {
    border: 1px solid rgba(139, 123, 255, .52) !important;
    border-radius: 12px !important;
    background: linear-gradient(120deg, rgba(30, 32, 78, .82), rgba(11, 18, 42, .9)) !important;
    color: #e8eaff !important;
}
</style>
"""


def _webcam_heading(icon, title):
    """Render a consistent cyan-to-neon-purple section heading."""
    st.markdown(
        f"""
        <div class="video-section-heading">
            <span class="video-heading-icon">{icon}</span>
            <span class="video-heading-text">{html.escape(title)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _webcam_stat_card(icon, label, value, detail=""):
    """Return compact HTML for one glossy live status tile.

    Keep this fragment free of blank lines so Streamlit's Markdown parser
    treats the complete grid as HTML instead of displaying source text.
    """
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_detail = html.escape(str(detail))
    return (
        '<div class="webcam-stat-card">'
        f'<div class="webcam-stat-icon">{icon}</div>'
        f'<div class="webcam-stat-label">{safe_label}</div>'
        f'<div class="webcam-stat-value">{safe_value}</div>'
        f'<div class="webcam-stat-detail">{safe_detail}</div>'
        '</div>'
    )


def show_webcam_page(model_name, confidence):
    st.markdown(WEBCAM_CSS, unsafe_allow_html=True)

    # Keep the title, controls, live status, and camera feed inside one panel.
    with st.container(border=True, key="webcam_detection_panel"):
        _webcam_heading("◉", "Real-Time Webcam Detection")
        st.write("Run live object detection from your camera with your selected YOLO model.")

        start_camera = st.button("▶  Start Camera", key="webcam_start_camera")

        if not start_camera:
            # No separate info/alert card below the Start Camera button.
            return

        st.session_state["_webcam_explorer_rendered"] = False
        detector = Detector(f"models/{model_name.lower()}.pt", confidence)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Unable to access webcam. Check camera permissions and try again.")
            cap.release()
            return

        status_placeholder = st.empty()
        frame_placeholder = st.empty()
        stop_button_placeholder = st.empty()

        kpi_placeholder = st.empty()
        analytics_placeholder = st.empty()
        summary_placeholder = st.empty()
        explorer_placeholder = st.empty()
        live_objects_placeholder = st.empty()

        stop_button = stop_button_placeholder.button(
            "■  Stop Camera", key="webcam_stop_camera"
        )

        last_dashboard_update = time.time()
        prev_frame_time = time.time()

        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    st.error("Unable to read a frame from the webcam.")
                    break

                webcam_summary = detector.detect_webcam(frame)
                object_counts = webcam_summary["object_counts"]
                object_confidences = webcam_summary["object_confidences"]
                confidence_scores = webcam_summary["confidence_scores"]
                total_objects = webcam_summary["total_objects"]
                total_classes = webcam_summary["unique_classes"]
                results = webcam_summary["results"]

                save_detection_summary(
                source="Webcam",
                object_counts=object_counts,
                confidence_scores=confidence_scores,
                total_objects=total_objects,
                model_name=model_name,
            )
                if total_objects == 0:
                    summary = {
                        "Detection Status": "Completed Successfully",
                        "Total Objects": 0,
                        "Unique Classes": 0,
                        "Model Used": model_name,
                        "Detection Quality": "No Objects",
                        "Dominant Object": "None",
                        "Average Confidence": 0,
                        "Scene Complexity": "Low",
                        "Detection Diversity": "Low",
                        "AI Observation": "No objects are currently visible in the webcam.",
                    }
                else:
                    summary = generate_ai_summary(
                        object_counts, confidence_scores, model_name
                    )

                annotated_frame = results[0].plot()
                # Keep the latest processed frame available to the Dashboard.
                save_detection_preview(
                    source="Webcam",
                    original_image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                    detected_image=cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
                    object_counts=object_counts,
                    confidence_scores=confidence_scores,
                    model_name=model_name,
                    scene_summary=generate_ai_summary(object_counts, confidence_scores, model_name),
                )
                frame_placeholder.image(
                    annotated_frame,
                    channels="BGR",
                    use_container_width=True,
                )

                current_time = time.time()
                if current_time - last_dashboard_update >= 1:
                    avg_conf = (
                        sum(confidence_scores) / len(confidence_scores) * 100
                        if confidence_scores
                        else 0
                    )
                    now = time.time()
                    fps = 1 / max(now - prev_frame_time, 0.001)
                    prev_frame_time = now

                    with status_placeholder.container():
                        stats_html = (
                            '<div class="webcam-stat-grid">'
                            + _webcam_stat_card("●", "Status", "LIVE", "Camera active")
                            + _webcam_stat_card("▣", "Model", model_name, "Selected YOLO model")
                            + _webcam_stat_card("◎", "Objects", total_objects, "Objects in current frame")
                            + _webcam_stat_card("ϟ", "FPS", f"{fps:.1f}", "Frames per second")
                            + '</div>'
                        )
                        st.markdown(stats_html, unsafe_allow_html=True)

                    with live_objects_placeholder.container():
                        _webcam_heading("◎", "Top Live Detections")
                        if object_counts:
                            sorted_objects = sorted(
                                object_counts.items(),
                                key=lambda item: item[1],
                                reverse=True,
                            )
                            cols = st.columns(min(4, len(sorted_objects)))
                            for i, (obj, count) in enumerate(sorted_objects[:4]):
                                conf_values = object_confidences.get(obj, [])
                                object_avg_conf = (
                                    sum(conf_values) / len(conf_values) * 100
                                    if conf_values
                                    else 0
                                )
                                with cols[i]:
                                    info_card(
                                        "◎",
                                        obj.title(),
                                        count,
                                        f"{object_avg_conf:.1f}% Avg Confidence",
                                    )
                        else:
                            st.caption("No objects detected in the current frame.")

                    with kpi_placeholder.container():
                        _webcam_heading("▦", "Live Detection Summary")
                        c1, c2, c3, c4 = st.columns(4)
                        with c1:
                            info_card("⬡", "Objects", total_objects, "Detected Objects")
                        with c2:
                            info_card("◎", "Classes", total_classes, "Unique Classes")
                        with c3:
                            info_card("▣", "Model", model_name, "YOLO Model")
                        with c4:
                            info_card("●", "Status", "LIVE", "Detection Running")

                    with summary_placeholder.container():
                        _webcam_heading("✧", "Live AI Detection Summary")
                        ai_summary_card(summary)

                    # detection_cards creates Streamlit expanders. Rendering it on every
                    # frame inside this loop re-creates the same widget keys and triggers
                    # StreamlitDuplicateElementKey. Render the explorer once per camera run.
                    if not st.session_state.get("_webcam_explorer_rendered", False):
                        with explorer_placeholder.container():
                            _webcam_heading("⌕", "Detection Explorer")
                            detection_cards(
                                object_counts,
                                object_confidences,
                                max_objects=min(5, len(object_counts)),
                            )
                        st.session_state["_webcam_explorer_rendered"] = True

                    with analytics_placeholder.container():
                        _webcam_heading("⌁", "Live Detection Analytics")
                        st.caption("Analytics update as new webcam frames are processed.")
                        col1, col2 = st.columns(2)
                        with col1:
                            object_bar_chart(
                                object_counts,
                                chart_key=f"webcam_bar_{int(current_time)}",
                            )
                        with col2:
                            object_pie_chart(
                                object_counts,
                                chart_key=f"webcam_pie_{int(current_time)}",
                            )

                        col3, col4 = st.columns(2)
                        with col3:
                            fig = confidence_histogram(confidence_scores)
                            st.plotly_chart(
                                fig,
                                use_container_width=True,
                                key=f"webcam_hist_{int(current_time)}",
                            )
                        with col4:
                            fig = confidence_gauge(confidence_scores)
                            st.plotly_chart(
                                fig,
                                use_container_width=True,
                                key=f"webcam_gauge_{int(current_time)}",
                            )

                    last_dashboard_update = current_time

                if stop_button:
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

        frame_placeholder.empty()
        status_placeholder.empty()
        stop_button_placeholder.empty()
        st.markdown(
            """
            <div class="webcam-stat-card" style="max-width:340px;margin-top:14px;">
                <div class="webcam-stat-icon">✓</div>
                <div class="webcam-stat-label">Camera Status</div>
                <div class="webcam-stat-value">STOPPED</div>
                <div class="webcam-stat-detail">Webcam resources released</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Export the final annotated frame and the final frame's detection summary.
        _webcam_heading("⇩", "Export Live Detection")
        st.caption("Download the last processed webcam frame or its detection summary.")
        export_col1, export_col2 = st.columns(2)

        with export_col1:
            if "annotated_frame" in locals() and annotated_frame is not None:
                encoded_ok, encoded_frame = cv2.imencode(".jpg", annotated_frame)
                if encoded_ok:
                    st.download_button(
                        "⇩  Download Detected Snapshot",
                        data=encoded_frame.tobytes(),
                        file_name="visionai_webcam_detection.jpg",
                        mime="image/jpeg",
                        key="webcam_download_snapshot",
                    )
            else:
                st.caption("No processed frame is available to download yet.")

        with export_col2:
            if "webcam_summary" in locals():
                csv_buffer = io.StringIO()
                writer = csv.writer(csv_buffer)
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Model", model_name])
                writer.writerow(["Total objects in final frame", webcam_summary.get("total_objects", 0)])
                writer.writerow(["Unique classes in final frame", webcam_summary.get("unique_classes", 0)])
                writer.writerow(["Object class", "Count"])
                for object_name, count in webcam_summary.get("object_counts", {}).items():
                    writer.writerow([object_name, count])
                st.download_button(
                    "⇩  Download Detection Summary (CSV)",
                    data=csv_buffer.getvalue().encode("utf-8-sig"),
                    file_name="visionai_webcam_summary.csv",
                    mime="text/csv",
                    key="webcam_download_summary_csv",
                )
            else:
                st.caption("No detection summary is available to download yet.")
