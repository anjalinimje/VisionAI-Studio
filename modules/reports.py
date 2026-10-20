"""VisionAI Studio — Reports page.
Builds an exportable report from detection_history in Streamlit session state.
"""
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

REPORT_CSS = """

<style>
:root {
    color-scheme: dark;
}

.report-hero {
    padding: 24px 28px;
    margin: 2px 0 20px;
    border-radius: 20px;
    border: 1px solid rgba(139, 92, 246, .55);
    background:
        radial-gradient(ellipse at 95% 0%,
            rgba(124, 58, 237, .24), transparent 45%),
        linear-gradient(135deg, #0a1027, #130f30);
    box-shadow: 0 0 22px rgba(124, 58, 237, .10);
}

.report-eyebrow {
    color: #67e8f9;
    font-size: .82rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}



.report-title {
    background: linear-gradient(
        90deg,
        #C4B5FD 0%,
        #A855F7 45%,
        #67E8F9 100%
    );
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: #C4B5FD;
    filter: drop-shadow(0 0 8px rgba(168, 85, 247, 0.55));
    font-size: 2.25rem;
    line-height: 1.15;
    font-weight: 850;
    margin: 0;
}



.report-subtitle {
    color: #c1c9e8;
    font-size: 1.02rem;
    margin-top: 9px;
}


.report-panel-title {
    color: #E9D5FF;
    font-size: 1.15rem;
    font-weight: 800;
    text-shadow: 0 0 10px rgba(139, 92, 246, 0.25);
}


/* Neon-themed metric cards */

div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(21, 19, 57, 0.96),
        rgba(9, 16, 39, 0.98)
    );
    border: 1px solid rgba(139, 92, 246, 0.72);
    border-radius: 15px;
    padding: 14px 16px;
    box-shadow:
        0 0 9px rgba(124, 58, 237, 0.22),
        inset 0 0 14px rgba(124, 58, 237, 0.08);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: rgba(34, 211, 238, 0.85);
    box-shadow:
        0 0 16px rgba(124, 58, 237, 0.34),
        0 0 8px rgba(34, 211, 238, 0.14);
}

div[data-testid="stMetricValue"] {
    color: #F5F3FF !important;
    font-size: 1.8rem !important;
    text-shadow: 0 0 10px rgba(167, 139, 250, 0.22);
}


/* Dark source, model and time-range dropdowns */
div[data-testid="stSelectbox"] label {
    color: #d9ddf5 !important;
    font-size: .92rem !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #101832 !important;
    color: #f5f3ff !important;
    border: 1px solid rgba(139, 92, 246, .62) !important;
    border-radius: 10px !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] * {
    color: #f5f3ff !important;
}

/* Report table frame */

div[data-testid="stDataFrame"] {
    border: 1px solid rgba(168, 85, 247, 0.78) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 0 12px rgba(124, 58, 237, 0.20);
}


/* Purple download buttons with cyan hover */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(100deg, #6d28d9, #7c3aed) !important;
    color: #ffffff !important;
    border: 1px solid rgba(167, 139, 250, .8) !important;
    border-radius: 10px !important;
    font-weight: 750 !important;
    box-shadow: 0 0 13px rgba(124, 58, 237, .18);
}

div[data-testid="stDownloadButton"] button:hover {
    border-color: #67e8f9 !important;
    box-shadow: 0 0 18px rgba(34, 211, 238, .22);
}
</style>

"""

def _number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def _load_report_records():
    raw = st.session_state.get("detection_history", [])
    if not isinstance(raw, list):
        return []
    records = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        counts = item.get("object_counts", item.get("Object Counts", item.get("counts", {})))
        if not isinstance(counts, dict):
            counts = {}
        scores = item.get("confidence_scores", item.get("Confidence Scores", item.get("confidences", [])))
        if not isinstance(scores, (list, tuple)):
            scores = []
        score_pct = []
        for score in scores:
            try:
                value = float(score)
                score_pct.append(value * 100 if value <= 1 else value)
            except (TypeError, ValueError):
                continue
        total = item.get("total_objects", item.get("Total Objects"))
        if total is None:
            total = sum(_number(v) for v in counts.values())
        classes = item.get("unique_classes", item.get("total_classes"))
        if classes is None:
            classes = len([v for v in counts.values() if _number(v) > 0])
        records.append({
            "Timestamp": str(item.get("timestamp", item.get("created_at", item.get("time", "—")))),
            "Source": str(item.get("source", item.get("Source", "Detection"))).title(),
            "Objects": int(_number(total)),
            "Classes": int(_number(classes)),
            "Model": str(item.get("model_name", item.get("model", "Unknown"))),
            "Counts": {str(k): int(_number(v)) for k, v in counts.items()},
            "Average confidence (%)": sum(score_pct) / len(score_pct) if score_pct else None,
        })
    return records

def show_reports_page():
    st.markdown(REPORT_CSS, unsafe_allow_html=True)
    st.markdown("""
    <section class="report-hero">
      <div class="report-eyebrow">VISIONAI STUDIO · REPORTING CENTER</div>
      <h1 class="report-title">Detection Reports</h1>
      <div class="report-subtitle">Summarize saved object-detection sessions and export a report for review.</div>
    </section>
    """, unsafe_allow_html=True)

    records = _load_report_records()
    if not records:
        st.info("No saved detection sessions are available yet. Run an Image, Video, or Webcam detection first.")
        st.caption("This report uses history currently stored in Streamlit session state. For reports that survive app restarts, history must be stored in a database or file.")
        return

    f1, f2, f3 = st.columns([1, 1, 1.5], gap="medium")
    with f1:
        source = st.selectbox("Source", ["All sources", "Image", "Video", "Webcam"], key="reports_source")
    with f2:
        models = ["All models"] + sorted({r["Model"] for r in records})
        model = st.selectbox("Model", models, key="reports_model")
    with f3:
        period = st.selectbox("Time range", ["All available history", "Last 24 hours", "Last 7 days", "Last 30 days"], key="reports_time_range")

    filtered = records
    if source != "All sources":
        filtered = [r for r in filtered if r["Source"].lower() == source.lower()]
    if model != "All models":
        filtered = [r for r in filtered if r["Model"] == model]
    if period != "All available history":
        cutoff = datetime.now() - timedelta(days={"Last 24 hours": 1, "Last 7 days": 7, "Last 30 days": 30}[period])
        dated = []
        for row in filtered:
            try:
                if datetime.fromisoformat(row["Timestamp"]) >= cutoff:
                    dated.append(row)
            except (ValueError, TypeError):
                continue
        filtered = dated

    class_totals = {}
    for row in filtered:
        for name, count in row["Counts"].items():
            class_totals[name] = class_totals.get(name, 0) + count
    sessions = len(filtered)
    objects = sum(r["Objects"] for r in filtered)
    class_count = len([k for k, v in class_totals.items() if v > 0])
    confidence = [r["Average confidence (%)"] for r in filtered if r["Average confidence (%)"] is not None]
    avg_conf = sum(confidence) / len(confidence) if confidence else None

    st.markdown('<div class="report-panel-title">Report overview</div>', unsafe_allow_html=True)
    a, b, c, d = st.columns(4, gap="medium")
    a.metric("Detection sessions", sessions)
    b.metric("Objects detected", objects)
    c.metric("Object classes", class_count)
    d.metric("Avg. confidence", f"{avg_conf:.1f}%" if avg_conf is not None else "—")

    if not filtered:
        st.warning("No sessions match these filters. Try a wider time range or another source/model.")
        return

    
    st.markdown('<div class="report-panel-title" style="margin-top:22px">Session report</div>', unsafe_allow_html=True)
    rows = [{
        "Date & time": r["Timestamp"], "Source": r["Source"], "Objects": r["Objects"], "Classes": r["Classes"],
        "Average confidence": f'{r["Average confidence (%)"]:.1f}%' if r["Average confidence (%)"] is not None else "—",
        "Model": r["Model"],
    } for r in reversed(filtered)]
    table = pd.DataFrame(rows)
    styled_table = (
    table.style
    .set_table_styles([
        {
            "selector": "table",
            "props": [
                ("background-color", "#0B1127"),
                ("color", "#F5F3FF"),
                ("border-collapse", "collapse"),
                ("width", "100%"),
                ("border", "1px solid #7C3AED"),
            ],
        },
        {
            "selector": "th",
            "props": [
                ("background-color", "#211344"),
                ("color", "#67E8F9"),
                ("padding", "12px"),
                ("text-align", "left"),
                ("border-bottom", "1px solid #7C3AED"),
            ],
        },
        {
            "selector": "td",
            "props": [
                ("background-color", "#0B1127"),
                ("color", "#F5F3FF"),
                ("padding", "12px"),
                ("border-bottom", "1px solid #29204A"),
            ],
        },
    ])
    .hide(axis="index")
)

    st.markdown(
    styled_table.to_html(),
    unsafe_allow_html=True,
)

    st.markdown('<div class="report-panel-title" style="margin-top:22px">Export report</div>', unsafe_allow_html=True)
    st.download_button("Download session report (CSV)", table.to_csv(index=False).encode("utf-8"), "visionai_detection_report.csv", "text/csv", key="reports_download_csv")
    lines = [
        "VISIONAI STUDIO — DETECTION REPORT", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Source filter: {source}", f"Model filter: {model}", f"Time range: {period}", "",
        f"Detection sessions: {sessions}", f"Objects detected: {objects}", f"Object classes: {class_count}",
        f"Average confidence: {f'{avg_conf:.1f}%' if avg_conf is not None else 'Not available'}", "", "OBJECT CLASS BREAKDOWN",
    ]
    lines.extend(f"{name}: {count}" for name, count in sorted(class_totals.items(), key=lambda item: item[1], reverse=True))
    lines.extend(["", "SESSION DETAILS", table.to_string(index=False)])
    st.download_button("Download text summary (TXT)", "\n".join(lines).encode("utf-8"), "visionai_detection_report.txt", "text/plain", key="reports_download_txt")
