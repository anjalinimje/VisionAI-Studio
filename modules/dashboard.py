"""
VisionAI Studio — Dashboard
------------------------------------------------
Replace your existing modules/dashboard.py with this file.

Data contract:
- Detection pages should call save_detection_summary(source=..., object_counts=...,
  confidence_scores=..., total_objects=..., model_name=..., timestamp=...)
  after a detection session completes.
- The dashboard also reads legacy summary keys and history lists from st.session_state.
"""

from collections import Counter
from datetime import datetime
import html
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ------------------------------- Theme ---------------------------------------
CSS = """
<style>
.dashboard-hero{position:relative;overflow:hidden;padding:27px 30px;margin:2px 0 22px;
border:1px solid rgba(139,92,246,.72);border-radius:24px;
background:radial-gradient(ellipse at 92% 8%,rgba(124,58,237,.35),transparent 38%),
radial-gradient(ellipse at 4% 100%,rgba(6,182,212,.17),transparent 42%),
linear-gradient(135deg,rgba(12,15,43,.98),rgba(24,13,61,.95));
box-shadow:0 0 24px rgba(124,58,237,.18),inset 0 1px 0 rgba(255,255,255,.1)}
.dashboard-eyebrow{color:#a5f3fc;text-transform:uppercase;letter-spacing:2.2px;font-size:.72rem;font-weight:800;margin-bottom:8px}
.dashboard-title{margin:0;font-size:clamp(1.8rem,3vw,2.55rem);line-height:1.12;font-weight:850;letter-spacing:-.8px;
background:linear-gradient(95deg,#22d3ee 0%,#818cf8 48%,#e879f9 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.dashboard-subtitle{color:#d8def7;margin-top:10px;font-size:.98rem;max-width:760px}
.preview-label{font-size:.65rem;font-weight:850;letter-spacing:1.4px;color:#67e8f9;margin:5px 0 9px}.scene-summary{position:relative;border:1px solid rgba(34,211,238,.28);border-radius:15px;padding:16px 15px 16px 44px;background:radial-gradient(circle at 0% 0%,rgba(124,58,237,.24),transparent 55%),rgba(8,20,46,.75);color:#e3e8ff;line-height:1.65;font-size:.88rem;min-height:130px}.scene-spark{position:absolute;left:14px;top:14px;color:#67e8f9;font-size:1.1rem}.class-chip-row{display:flex;flex-wrap:wrap;gap:7px}.class-chip{display:inline-flex;align-items:center;gap:9px;padding:6px 9px;border:1px solid rgba(139,92,246,.48);border-radius:999px;background:rgba(109,40,217,.16);color:#e9e7ff;font-size:.73rem}.class-chip em{font-style:normal;color:#67e8f9;font-weight:850}.source-status-row{display:flex;flex-wrap:wrap;gap:10px;margin:-7px 0 20px}.source-status{display:flex;align-items:center;gap:8px;padding:9px 13px;border-radius:12px;background:rgba(16,22,54,.74);border:1px solid rgba(139,92,246,.32);color:#dce3ff;font-size:.78rem;font-weight:750}.source-status i{width:7px;height:7px;border-radius:50%;display:inline-block}.source-status b{font-size:.64rem;letter-spacing:.8px;margin-left:5px}.dashboard-pill{display:inline-flex;align-items:center;gap:7px;margin-top:17px;padding:7px 12px;border-radius:999px;color:#ddd6fe;font-size:.76rem;font-weight:750;background:rgba(109,40,217,.22);border:1px solid rgba(167,139,250,.52)}
.dash-section{display:flex;align-items:center;gap:11px;margin:25px 0 13px;font-size:1.2rem;font-weight:850;color:#f5f3ff}
.dash-section-icon{width:37px;height:37px;display:inline-flex;align-items:center;justify-content:center;border-radius:12px;color:#67e8f9;font-size:1.05rem;border:1px solid rgba(139,92,246,.85);background:linear-gradient(145deg,rgba(91,33,182,.55),rgba(8,47,73,.45));box-shadow:0 0 17px rgba(124,58,237,.22),inset 0 1px 0 rgba(255,255,255,.15)}
.dash-panel{border:1px solid rgba(139,92,246,.48);border-radius:19px;padding:15px 16px 9px;background:linear-gradient(145deg,rgba(19,20,58,.72),rgba(10,16,39,.76));box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 0 15px rgba(124,58,237,.08)}
.dash-panel-title{color:#e9e7ff;font-size:.96rem;font-weight:800;margin:0 0 3px}
.dash-panel-caption{color:#9ca8d2;font-size:.75rem;margin-bottom:7px}
.dash-empty{border:1px dashed rgba(139,92,246,.65);border-radius:17px;padding:23px 22px;background:linear-gradient(135deg,rgba(30,27,75,.58),rgba(8,18,43,.58));color:#d6d9f4;text-align:center}
.dash-empty-title{font-weight:800;color:#e9d5ff;margin-bottom:5px}
.dash-empty-text{font-size:.85rem;color:#aeb9df}
.ring-wrap{border:1px solid rgba(139,92,246,.55);border-radius:20px;padding:10px 10px 13px;text-align:center;background:radial-gradient(circle at 50% 30%,rgba(124,58,237,.16),transparent 58%),linear-gradient(145deg,rgba(25,20,61,.86),rgba(9,17,43,.92));box-shadow:0 0 18px rgba(124,58,237,.1),inset 0 1px 0 rgba(255,255,255,.06)}
.ring-graphic{width:100%;max-width:178px;margin:0 auto}.ring-graphic svg{display:block;width:100%;height:auto;overflow:visible}.ring-label{color:#e9e7ff;font-size:.9rem;font-weight:850;margin-top:1px}
.ring-note{color:#9ca8d2;font-size:.72rem;margin-top:4px;min-height:30px}.ring-track{height:3px;max-width:150px;margin:11px auto 0;border-radius:99px;background:rgba(139,92,246,.16);overflow:hidden}.ring-track span{display:block;height:100%;border-radius:99px;box-shadow:0 0 10px rgba(34,211,238,.5)}
div[data-testid="stDataFrame"]{border:1px solid rgba(139,92,246,.42);border-radius:14px;overflow:hidden}div[data-testid="stDownloadButton"] button{border:1px solid rgba(167,139,250,.8)!important;background:linear-gradient(110deg,#5b21b6,#6d28d9 55%,#4338ca)!important;color:#fff!important;border-radius:12px!important;font-weight:800!important;box-shadow:0 0 16px rgba(124,58,237,.22)!important}

/* Dashboard readability improvements */
.dash-section {
    font-size: 1.45rem !important;
}

.minimal-panel-title,
.dash-panel-title {
    font-size: 1.1rem !important;
}

.minimal-panel-subtitle,
.dash-panel-caption {
    font-size: 0.9rem !important;
}

.ring-label {
    font-size: 1.05rem !important;
}

.ring-note {
    font-size: 0.85rem !important;
}

.scene-summary {
    font-size: 1rem !important;
    line-height: 1.8 !important;
}

div[data-testid="stDataFrame"] {
    font-size: 0.95rem !important;
}


/* ===== VisionAI Studio: Typography Improvements ===== */

/* Small brand heading: VISIONAI STUDIO · COMPUTER VISION */
.minimal-eyebrow,
.dashboard-eyebrow {
    font-size: 0.9rem !important;
    letter-spacing: 2px;
    line-height: 1.5;
}

/* Main dashboard heading */
.minimal-title,
.dashboard-title {
    font-size: clamp(2rem, 3.5vw, 2.7rem) !important;
    line-height: 1.2;

background: linear-gradient(90deg, #C4B5FD 0%, #A855F7 48%, #22D3EE 100%);
-webkit-background-clip: text;
background-clip: text;
-webkit-text-fill-color: transparent;
filter: drop-shadow(0 0 8px rgba(168, 85, 247, 0.4));

}

/* Subtitle below the main heading */
.minimal-subtitle,
.dashboard-subtitle {
    font-size: 1rem !important;
    line-height: 1.6;
}

/* Section titles */
.minimal-panel-title {
    font-size: 1.2rem !important;
    line-height: 1.4;
    font-weight: 800;
}

/* Descriptions below section titles */
.minimal-panel-subtitle {
    font-size: 0.95rem !important;
    line-height: 1.5;
}

/* Detection Source and other Streamlit field labels */
div[data-testid="stWidgetLabel"] p {
    font-size: 1rem !important;
    line-height: 1.5;
    font-weight: 600;
}

/* DETECTED OBJECTS heading */
.preview-label {
    font-size: 0.9rem !important;
    letter-spacing: 1.5px;
}

/* Scene summary text */
.scene-summary {
    font-size: 1rem !important;
    line-height: 1.7;
}

/* Object labels and count badges */
.class-chip {
    font-size: 0.85rem !important;
}


</style>
"""


def _section(title, icon="◈"):
    st.markdown(
        f'<div class="dash-section"><span class="dash-section-icon">{icon}</span>'
        f'<span>{html.escape(title)}</span></div>',
        unsafe_allow_html=True,
    )


def _panel_title(title, caption=""):
    st.markdown(
        f'<div class="dash-panel-title">{html.escape(title)}</div>'
        + (f'<div class="dash-panel-caption">{html.escape(caption)}</div>' if caption else ""),
        unsafe_allow_html=True,
    )


def _as_dict(value):
    return value if isinstance(value, dict) else {}


def _num(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def save_detection_summary(
    source,
    object_counts,
    confidence_scores=None,
    total_objects=None,
    model_name="Unknown",
    timestamp=None,
    extra=None,
):
    """
    Save one completed Image / Video / Webcam run to shared Streamlit session state.
    Call this once per completed run (not once per video frame).
    """
    source = str(source).strip().title()
    if source not in {"Image", "Video", "Webcam"}:
        source = "Detection"
    counts = {str(k): int(_num(v)) for k, v in _as_dict(object_counts).items()}
    scores = [_num(s) for s in (confidence_scores or []) if s is not None]
    record = {
        "source": source,
        "object_counts": counts,
        "confidence_scores": scores,
        "total_objects": int(_num(total_objects, sum(counts.values()))) if total_objects is not None else sum(counts.values()),
        "unique_classes": len([k for k, v in counts.items() if v > 0]),
        "model_name": str(model_name or "Unknown"),
        "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if isinstance(extra, dict):
        record.update(extra)
    history = st.session_state.get("detection_history", [])
    if not isinstance(history, list):
        history = []
    # Avoid adding an exact duplicate on Streamlit reruns.
    signature = json.dumps(record, sort_keys=True, default=str)
    existing = {json.dumps(x, sort_keys=True, default=str) for x in history if isinstance(x, dict)}
    if signature not in existing:
        history.append(record)
    st.session_state["detection_history"] = history
    # Keep latest named summaries available to the dashboard and any other pages.
    st.session_state[f"{source.lower()}_summary"] = record
    return record



def _build_scene_summary(source, object_counts, confidence_scores=None):
    """Create a grounded, local summary from actual detections; no fabricated AI claims."""
    counts = {str(k): int(_num(v)) for k, v in _as_dict(object_counts).items() if _num(v) > 0}
    total = sum(counts.values())
    classes = len(counts)
    scores = [_num(s) for s in (confidence_scores or []) if s is not None]
    scores_pct = [s * 100 if s <= 1 else s for s in scores]
    avg = sum(scores_pct) / len(scores_pct) if scores_pct else None
    if total == 0:
        return f"The {source.lower()} analysis did not return any objects above the model's detection threshold. Try a clearer frame or adjust the confidence threshold."
    top = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3]
    top_text = ", ".join(f"{name} ({count})" for name, count in top)
    summary = f"The {source.lower()} analysis detected {total} object{'s' if total != 1 else ''} across {classes} class{'es' if classes != 1 else ''}. Most frequent: {top_text}."
    if avg is not None:
        summary += f" Mean detection confidence is {avg:.1f}%."
        if avg >= 80:
            summary += " Overall confidence is strong for this run."
        elif avg >= 55:
            summary += " Confidence is mixed; review lower-confidence boxes."
        else:
            summary += " Confidence is relatively low; inspect the preview before relying on these detections."
    return summary


def save_detection_preview(
    source,
    original_image=None,
    detected_image=None,
    object_counts=None,
    confidence_scores=None,
    model_name="Unknown",
    scene_summary=None,
    timestamp=None,
):
    """
    Store the latest original/detected preview for the dashboard.
    Pass a PIL image or a NumPy image array. Call after a successful detection run.
    """
    source = str(source).strip().title()
    if source not in {"Image", "Video", "Webcam"}:
        source = "Detection"
    counts = _as_dict(object_counts)
    summary = scene_summary or _build_scene_summary(source, counts, confidence_scores)
    payload = {
        "source": source,
        "original_image": original_image,
        "detected_image": detected_image,
        "object_counts": dict(counts),
        "confidence_scores": list(confidence_scores or []),
        "model_name": str(model_name or "Unknown"),
        "scene_summary": str(summary),
        "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state["latest_detection_preview"] = payload
    return payload


def _extract_records():
    records = []
    for key in ("detection_history", "visionai_history", "detection_sessions",
                "analytics_history", "history_records", "detection_records"):
        value = st.session_state.get(key)
        if isinstance(value, list):
            records.extend(dict(x) for x in value if isinstance(x, dict))

    for key, source in (
        ("image_summary", "Image"), ("video_summary", "Video"), ("webcam_summary", "Webcam"),
        ("last_image_detection", "Image"), ("last_video_detection", "Video"),
        ("last_webcam_detection", "Webcam"),
    ):
        value = st.session_state.get(key)
        if isinstance(value, dict) and value:
            row = dict(value)
            row.setdefault("source", source)
            row.setdefault("timestamp", row.get("time", "Latest session"))
            records.append(row)

    # Deduplicate records which are exposed through both history and latest-summary keys.
    unique, seen = [], set()
    for row in records:
        signature = json.dumps(row, sort_keys=True, default=str)
        if signature not in seen:
            seen.add(signature)
            unique.append(row)
    return unique


def _normalise(record):
    source = str(record.get("source", record.get("Source", record.get("type", "Detection")))).title()
    counts = _as_dict(record.get("object_counts", record.get("Object Counts", record.get("counts", {}))))
    raw_scores = record.get("confidence_scores", record.get("Confidence Scores", record.get("confidences", [])))
    if isinstance(raw_scores, (list, tuple)):
        scores = [_num(x) for x in raw_scores if x is not None]
    else:
        scores = []
    total = record.get("total_objects", record.get("Total Objects", record.get("objects")))
    total = int(_num(total, sum(int(_num(v)) for v in counts.values())))
    classes = record.get("unique_classes", record.get("total_classes", record.get("Unique Classes")))
    classes = int(_num(classes, len([k for k, v in counts.items() if _num(v) > 0])))
    model = str(record.get("model_name", record.get("model", record.get("Model Used", "Unknown"))))
    timestamp = str(record.get("timestamp", record.get("created_at", record.get("time", "—"))))
    avg = sum(scores) / len(scores) * 100 if scores else _num(record.get("average_confidence", 0))
    # Preserve scores in their native 0..1 or 0..100 form; convert only for charting.
    return {"Source": source, "Objects": total, "Classes": classes, "Model": model,
            "Average confidence": avg, "Timestamp": timestamp, "Counts": counts, "Scores": scores}


def _theme(fig, height=320):
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce3ff", family="Inter, Arial, sans-serif", size=12),
        margin=dict(l=12, r=12, t=24, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5f5")),
        xaxis=dict(gridcolor="rgba(139,92,246,.13)", zerolinecolor="rgba(139,92,246,.2)"),
        yaxis=dict(gridcolor="rgba(139,92,246,.13)", zerolinecolor="rgba(139,92,246,.2)"),
    )
    return fig


def _ring(label, value, maximum, suffix="", note="", color="#A855F7"):
    """Render a self-contained SVG intelligence ring (avoids broken cross-block HTML)."""
    maximum = max(float(maximum), 1.0)
    numeric_value = max(0.0, min(float(value), maximum))
    ratio = numeric_value / maximum
    radius = 42
    circumference = 2 * 3.141592653589793 * radius
    dash = circumference * ratio
    display_value = f"{numeric_value:,.0f}{suffix}" if suffix != "%" else f"{numeric_value:.0f}%"
    if suffix == "/3":
        display_value = f"{numeric_value:.0f}/3"
    safe_color = color if color.startswith("#") and len(color) == 7 else "#A855F7"
    st.markdown(f"""
    <div class="ring-wrap">
      <div class="ring-graphic">
        <svg viewBox="0 0 120 120" role="img" aria-label="{html.escape(label)}: {html.escape(display_value)}">
          <defs>
            <filter id="glow-{html.escape(label.lower().replace(' ', '-'))}">
              <feGaussianBlur stdDeviation="3.5" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <linearGradient id="grad-{html.escape(label.lower().replace(' ', '-'))}" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="{safe_color}"/>
              <stop offset="100%" stop-color="#22D3EE"/>
            </linearGradient>
          </defs>
          <circle cx="60" cy="60" r="{radius}" fill="none" stroke="rgba(139,92,246,.17)" stroke-width="9"/>
          <circle cx="60" cy="60" r="{radius}" fill="none" stroke="url(#grad-{html.escape(label.lower().replace(' ', '-'))})"
            stroke-width="9" stroke-linecap="round" stroke-dasharray="{dash:.2f} {circumference:.2f}"
            transform="rotate(-90 60 60)" filter="url(#glow-{html.escape(label.lower().replace(' ', '-'))})"/>
          <circle cx="60" cy="60" r="31" fill="rgba(10,13,37,.8)" stroke="rgba(103,232,249,.13)" stroke-width="1"/>
          <text x="60" y="65" text-anchor="middle" fill="#F5F3FF" font-size="19" font-weight="800">{html.escape(display_value)}</text>
          <circle cx="60" cy="18" r="3" fill="#67E8F9"/>
        </svg>
      </div>
      <div class="ring-label">{html.escape(label)}</div>
      <div class="ring-note">{html.escape(note)}</div>
      <div class="ring-track"><span style="width:{ratio*100:.1f}%;background:linear-gradient(90deg,{safe_color},#22D3EE)"></span></div>
    </div>
    """, unsafe_allow_html=True)


def show_dashboard():
    """Minimal & Modern dashboard: glowing rings, latest preview, scene summary, and concise history."""
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .minimal-hero{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:22px 25px;margin:2px 0 18px;border:1px solid rgba(139,92,246,.42);border-radius:20px;background:radial-gradient(ellipse at 95% 0%,rgba(124,58,237,.22),transparent 42%),linear-gradient(135deg,rgba(10,16,39,.98),rgba(19,15,48,.96));box-shadow:0 0 22px rgba(124,58,237,.10)}
    .minimal-eyebrow{color:#67e8f9;font-size:.68rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}.minimal-title{color:#f5f3ff;font-size:clamp(1.7rem,3vw,2.25rem);line-height:1.12;font-weight:850;letter-spacing:-.7px;margin:0}.minimal-subtitle{color:#aeb9df;font-size:.88rem;margin-top:8px}.minimal-live{white-space:nowrap;padding:8px 11px;border-radius:999px;border:1px solid rgba(34,211,238,.28);background:rgba(8,145,178,.10);color:#a5f3fc;font-size:.72rem;font-weight:800}.minimal-live i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#22d3ee;margin-right:7px;box-shadow:0 0 9px #22d3ee}.minimal-panel-title{color:#e9e7ff;font-size:.94rem;font-weight:800;margin-bottom:4px}.minimal-panel-subtitle{color:#8f9bc5;font-size:.73rem;margin-bottom:12px}.minimal-empty{min-height:235px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:22px;border:1px dashed rgba(139,92,246,.42);border-radius:14px;color:#aeb9df;background:rgba(12,17,43,.42)}.minimal-empty strong{color:#e9d5ff;font-size:1rem;margin-bottom:6px}
    </style>
    <section class="minimal-hero"><div><div class="minimal-eyebrow">VISIONAI STUDIO · COMPUTER VISION</div><h1 class="minimal-title">Detection Dashboard</h1><div class="minimal-subtitle">A clear overview of your latest detections and model activity.</div></div><div class="minimal-live"><i></i>INTELLIGENCE CENTER</div></section>
    """, unsafe_allow_html=True)

    records = [_normalise(r) for r in _extract_records()]
    source_options = ["All sources", "Image", "Video", "Webcam"]
    selected_source = st.selectbox("Detection source", source_options, key="visionai_dashboard_source_filter")
    filtered = records if selected_source == "All sources" else [r for r in records if r["Source"].lower() == selected_source.lower()]

    counts = Counter()
    all_scores = []
    for row in filtered:
        counts.update({str(k): int(_num(v)) for k, v in row["Counts"].items()})
        all_scores.extend(row["Scores"])
    total_objects = sum(row["Objects"] for row in filtered)
    total_classes = len([name for name, value in counts.items() if value > 0])
    if all_scores:
        avg_conf = sum(score * 100 if score <= 1 else score for score in all_scores) / len(all_scores)
    else:
        confs = [row["Average confidence"] for row in filtered if row["Average confidence"]]
        avg_conf = sum(confs) / len(confs) if confs else 0
        if 0 < avg_conf <= 1:
            avg_conf *= 100
    avg_conf = min(avg_conf, 100)
    sources_present = len({row["Source"] for row in filtered})
    top_class, top_count = counts.most_common(1)[0] if counts else ("—", 0)

    # Keep the existing intelligence-ring visual, but make it a compact overview row.
    ring_cols = st.columns(4, gap="medium")
    ring_values = [
        ("Objects detected", total_objects, max(total_objects, 10), "", "Across saved runs", "#A855F7"),
        ("Unique classes", total_classes, max(total_classes, 10), "", "Object categories", "#22D3EE"),
        ("Avg. confidence", avg_conf, 100, "%", "Mean confidence", "#C084FC"),
        ("Sources active", sources_present, 3, "/3", "Image · Video · Webcam", "#38BDF8"),
    ]
    for col, args in zip(ring_cols, ring_values):
        with col:
            _ring(*args)

    preview = st.session_state.get("latest_detection_preview", {})
    preview_ok = isinstance(preview, dict) and (preview.get("original_image") is not None or preview.get("detected_image") is not None)
    visual_col, summary_col = st.columns([1.7, 1], gap="medium")
    with visual_col:
        with st.container(border=True):
            st.markdown('<div class="minimal-panel-title">Latest Detection Preview</div><div class="minimal-panel-subtitle">Visual evidence from your most recent run</div>', unsafe_allow_html=True)
            if preview_ok:
                detected = preview.get("detected_image")
                original = preview.get("original_image")
                st.image(detected if detected is not None else original, use_container_width=True)
                st.caption(f'{preview.get("source", "Detection")} · {preview.get("timestamp", "Latest run")} · Model: {preview.get("model_name", "Unknown")}')
                if original is not None and detected is not None:
                    with st.expander("View original image/frame"):
                        st.image(original, use_container_width=True)
            else:
                st.markdown('<div class="minimal-empty"><strong>No detection preview yet</strong><br/>Run Image, Video, or Webcam Detection and the latest saved preview will appear here.</div>', unsafe_allow_html=True)

    with summary_col:
        with st.container(border=True):
            st.markdown('<div class="minimal-panel-title">Scene Summary</div><div class="minimal-panel-subtitle">A compact summary of the latest result</div>', unsafe_allow_html=True)
            if preview_ok:
                preview_source = str(preview.get("source", "Detection"))
                preview_counts = _as_dict(preview.get("object_counts", {}))
                preview_summary = str(preview.get("scene_summary") or _build_scene_summary(preview_source, preview_counts, preview.get("confidence_scores", [])))
                st.markdown(f'<div class="scene-summary"><div class="scene-spark">✦</div>{html.escape(preview_summary)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="preview-label" style="margin-top:15px">DETECTED OBJECTS</div>', unsafe_allow_html=True)
                visible_counts = [(name, int(_num(value))) for name, value in preview_counts.items() if _num(value) > 0]
                if visible_counts:
                    chips = "".join(f'<span class="class-chip"><b>{html.escape(name)}</b><em>{value}</em></span>' for name, value in sorted(visible_counts, key=lambda item: item[1], reverse=True)[:10])
                    st.markdown(f'<div class="class-chip-row">{chips}</div>', unsafe_allow_html=True)
                else:
                    st.caption("Object counts were not saved for this preview.")
            else:
                st.markdown('<div class="minimal-empty"><strong>Waiting for a result</strong><br/>The scene summary and detected object labels will appear after your next detection.</div>', unsafe_allow_html=True)
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            m1.metric("Saved sessions", len(filtered))
            m2.metric("Top class", top_class if top_count else "—")

    # One simple chart keeps the dashboard informative without overwhelming the preview.
    if counts:
        chart_col, insight_col = st.columns([1.45, 1], gap="medium")
        with chart_col:
            with st.container(border=True):
                st.markdown('<div class="minimal-panel-title">Object Distribution</div><div class="minimal-panel-subtitle">Most common classes in the selected view</div>', unsafe_allow_html=True)
                chart_df = pd.DataFrame([{"Class": name, "Detections": value} for name, value in counts.most_common(8)])
                fig = px.bar(chart_df, x="Class", y="Detections", text="Detections", color="Detections", color_continuous_scale=["#312e81", "#7c3aed", "#22d3ee"])
                fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
                fig.update_coloraxes(showscale=False)
                st.plotly_chart(_theme(fig, 270), use_container_width=True, key="dashboard_class_bar")
        with insight_col:
            with st.container(border=True):
                st.markdown('<div class="minimal-panel-title">Quick Insights</div><div class="minimal-panel-subtitle">Based on saved detection sessions</div>', unsafe_allow_html=True)
                st.metric("Most detected class", top_class, f"{top_count} detections")
                st.metric("Object categories", total_classes)
                st.metric("Average confidence", f"{avg_conf:.1f}%" if avg_conf else "—")
    elif not filtered:
        st.info("Your dashboard is ready. Complete a detection run to populate the rings, preview, and insights.")

    
    st.markdown('<div style="text-align:center;color:#7885b5;font-size:.72rem;margin:22px 0 6px">VISIONAI STUDIO · COMPUTER VISION</div>', unsafe_allow_html=True)
