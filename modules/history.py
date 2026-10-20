"""VisionAI Studio — Detection History page."""
from collections import Counter
import pandas as pd
import streamlit as st

HISTORY_CSS = """
<style>
.history-hero{padding:24px 28px;margin:2px 0 20px;border-radius:20px;border:1px solid rgba(139,92,246,.55);background:radial-gradient(ellipse at 95% 0%,rgba(124,58,237,.24),transparent 45%),linear-gradient(135deg,rgba(10,16,39,.98),rgba(19,15,48,.96));}
.history-eyebrow{color:#67e8f9;font-size:.8rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:7px}

.history-title {
    background: linear-gradient(
        90deg,
        #C4B5FD 0%,
        #A855F7 48%,
        #67E8F9 100%
    );
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    color: #C4B5FD;
    filter: drop-shadow(0 0 8px rgba(168, 85, 247, 0.45));
    font-size: 2.25rem;
    line-height: 1.15;
    font-weight: 850;
    margin: 0;
}

.history-subtitle{color:#c1c9e8;font-size:1.02rem;margin-top:9px}
.history-panel-title{color:#eeeaff;font-size:1.15rem;font-weight:800}
div[data-testid="stMetricValue"]{font-size:1.8rem}

/* VisionAI Studio — History theme */
:root {
    color-scheme: dark;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-testid="stTextInput"] [data-baseweb="input"] {
    background: #101832 !important;
    color: #F5F3FF !important;
    border: 1px solid rgba(168, 85, 247, 0.75) !important;
    border-radius: 10px !important;
}

div[data-testid="stSelectbox"] [data-baseweb="select"] *,
div[data-testid="stTextInput"] input {
    color: #F5F3FF !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #8995BC !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151339, #091027);
    border: 1px solid rgba(139, 92, 246, 0.7);
    border-radius: 15px;
    padding: 14px;
    box-shadow: 0 0 12px rgba(124, 58, 237, 0.2);
}

div[data-testid="stMetricLabel"] p {
    color: #C1C9E8 !important;
}

div[data-testid="stMetricValue"] {
    color: #F5F3FF !important;
}


table.history-table {
    width: 100%;
    border-collapse: collapse;
    background: #0B1127;
    color: #F5F3FF;
    font-size: 0.92rem;
}

table.history-table th {
    background: #211344;
    color: #67E8F9;
    text-align: left;
    padding: 12px;
    border-bottom: 1px solid #7C3AED;
}

table.history-table td {
    background: #0B1127;
    color: #F5F3FF;
    padding: 11px;
    border-bottom: 1px solid #29204A;
}

table.history-table tbody tr:nth-child(even) td {
    background: #111832;
}

div[data-testid="stTextInput"] input {
    background: #101832 !important;
    color: #F5F3FF !important;
    border-color: #A855F7 !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #8995BC !important;
}

</style>
"""

def _safe_int(value, fallback=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback

def _records_from_session():
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
        source = str(item.get("source", item.get("Source", "Detection"))).title()
        total = item.get("total_objects", item.get("Total Objects"))
        if total is None:
            total = sum(_safe_int(v) for v in counts.values())
        classes = item.get("unique_classes", item.get("total_classes"))
        if classes is None:
            classes = len([v for v in counts.values() if _safe_int(v) > 0])
        confidence_values = []
        for score in scores:
            try:
                score = float(score)
                confidence_values.append(score * 100 if score <= 1 else score)
            except (TypeError, ValueError):
                continue
        avg = sum(confidence_values) / len(confidence_values) if confidence_values else None
        records.append({
            "Timestamp": str(item.get("timestamp", item.get("created_at", item.get("time", "—")))),
            "Source": source, "Objects": _safe_int(total), "Classes": _safe_int(classes),
            "Model": str(item.get("model_name", item.get("model", "Unknown"))),
            "Average confidence (%)": round(avg, 1) if avg is not None else None,
            "Object counts": {str(k): _safe_int(v) for k, v in counts.items()},
            "Confidence scores": list(scores),
        })
    return records

def show_history_page():
    st.markdown(HISTORY_CSS, unsafe_allow_html=True)
    st.markdown("""
    <section class="history-hero">
      <div class="history-eyebrow">VISIONAI STUDIO · ACTIVITY LOG</div>
      <h1 class="history-title">Detection History</h1>
      <div class="history-subtitle">Review previous detection sessions across images, videos, and webcam analysis.</div>
    </section>
    """, unsafe_allow_html=True)
    records = _records_from_session()
    if not records:
        st.info("No detection history is saved in this session yet. Run an Image, Video, or Webcam detection first.")
        st.caption("History currently uses Streamlit session state and may reset when the app session restarts.")
        return
    c1, c2 = st.columns([1, 2], gap="medium")
    with c1:
        source_filter = st.selectbox("Detection source", ["All sources", "Image", "Video", "Webcam"], key="history_source_filter")
    with c2:
        search_text = st.text_input("Search history", placeholder="Search object class or model…", key="history_search_text").strip().lower()
    filtered = records
    if source_filter != "All sources":
        filtered = [r for r in filtered if r["Source"].lower() == source_filter.lower()]
    if search_text:
        filtered = [r for r in filtered if search_text in r["Model"].lower() or search_text in r["Source"].lower() or any(search_text in name.lower() for name in r["Object counts"])]
    class_counts = Counter()
    for row in filtered:
        class_counts.update(row["Object counts"])
    m1, m2, m3, m4 = st.columns(4, gap="medium")
    m1.metric("Sessions", len(filtered))
    m2.metric("Objects detected", sum(r["Objects"] for r in filtered))
    m3.metric("Object classes", len([k for k, v in class_counts.items() if v > 0]))
    m4.metric("Sources represented", len({r["Source"] for r in filtered}))
    st.markdown('<div class="history-panel-title">Saved sessions</div>', unsafe_allow_html=True)
    if not filtered:
        st.warning("No history entries match these filters.")
        return
    rows = [{
        "Date & time": r["Timestamp"], "Source": r["Source"], "Objects": r["Objects"], "Classes": r["Classes"],
        "Avg. confidence": f'{r["Average confidence (%)"]:.1f}%' if r["Average confidence (%)"] is not None else "—",
        "Model": r["Model"],
    } for r in reversed(filtered)]
    table = pd.DataFrame(rows)
    st.markdown(
    table.to_html(
        index=False,
        escape=True,
        classes="history-table",
        border=0,
    ),
    unsafe_allow_html=True,
)
    
    