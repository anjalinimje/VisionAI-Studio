import html
import re
import streamlit as st


# Small inline SVGs keep the interface icons monochrome neon-purple instead of emoji.
_ICON_PATHS = {
    "📦": '<path d="M12 3 3.8 7.2 12 11.5 20.2 7.2 12 3Z"/><path d="M3.8 7.2V16.8L12 21l8.2-4.2V7.2M12 11.5V21"/>',
    "🎯": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "🤖": '<rect x="4" y="7" width="16" height="13" rx="3"/><path d="M12 3v4M8 12h.01M16 12h.01M9 16h6M2 12h2M20 12h2"/>',
    "⭐": '<path d="m12 3 2.7 5.5 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z"/>',
    "🏆": '<path d="M8 4h8v4a4 4 0 0 1-8 0V4ZM8 6H4v2a4 4 0 0 0 4 4M16 6h4v2a4 4 0 0 1-4 4M12 12v5M8 21h8M9 17h6v4H9z"/>',
    "📈": '<path d="M3 19V5M3 19h18M6 15l4-4 3 2 5-7M15 6h3v3"/>',
    "🌍": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18M5 6h14M5 18h14"/>',
    "🎨": '<path d="M12 3a9 9 0 1 0 0 18h1.5a2 2 0 0 0 1.4-3.4 1.8 1.8 0 0 1 1.3-3.1H18A3 3 0 0 0 21 11c0-4.4-4-8-9-8Z"/><circle cx="7.5" cy="10" r=".8"/><circle cx="10" cy="6.8" r=".8"/><circle cx="15" cy="7.5" r=".8"/>',
    "⬆️": '<path d="M12 20V4M6 10l6-6 6 6"/>',
    "⬇️": '<path d="M12 4v16M6 14l6 6 6-6"/>',
    "💡": '<path d="M9 18h6M10 21h4M8.5 14.5a7 7 0 1 1 7 0c-.8.6-1.2 1.3-1.3 2.5h-4.4c-.1-1.2-.5-1.9-1.3-2.5Z"/>',
    "🔎": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
    "📊": '<path d="M4 20V11h4v9M10 20V5h4v15M16 20v-7h4v7M2 20h20"/>',
}
def _icon_svg(icon, size=30):
    path = _ICON_PATHS.get(str(icon), '<circle cx="12" cy="12" r="8"/><path d="M8 12h8"/>')
    return (
        f'<svg class="neon-icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">'
        f'{path}</svg>'
    )


def info_card(icon, title, value, subtitle):
    """Render a compact neon-themed KPI card."""
    title_html = html.escape(str(title))
    value_html = html.escape(str(value))
    subtitle_html = html.escape(str(subtitle))
    icon_html = _icon_svg(icon, 30)

    st.markdown(
        f"""
        <div class="neon-info-card">
            <div class="neon-info-card-icon">{icon_html}</div>
            <div class="neon-info-card-title">{title_html}</div>
            <div class="neon-info-card-value">{value_html}</div>
            <div class="neon-info-card-subtitle">{subtitle_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def ai_summary_card(summary):
    """Render AI summary KPI cards and observation."""
    if summary.get("Detection Status") == "Completed Successfully":
        st.success("Detection Completed Successfully")
    else:
        st.error("Detection Failed")

    row1 = st.columns(4)
    cards_top = [
        ("📦", "Objects", summary.get("Total Objects", "—"), "Detected Objects"),
        ("🎯", "Classes", summary.get("Unique Classes", "—"), "Unique Classes"),
        ("🤖", "Model", summary.get("Model Used", "—"), "YOLO Model"),
        ("⭐", "Quality", summary.get("Detection Quality", "—"), "Detection Quality"),
    ]
    for col, card in zip(row1, cards_top):
        with col:
            info_card(*card)

    row2 = st.columns(4)
    cards_bottom = [
        ("🏆", "Dominant", summary.get("Dominant Object", "—"), "Most Detected Object"),
        ("📈", "Confidence", f'{summary.get("Average Confidence", "—")}%', "Average Confidence"),
        ("🌍", "Complexity", summary.get("Scene Complexity", "—"), "Scene Complexity"),
        ("🎨", "Diversity", summary.get("Detection Diversity", "—"), "Class Diversity"),
    ]
    for col, card in zip(row2, cards_bottom):
        with col:
            info_card(*card)

    st.markdown(
        f'<h3 class="neon-section-heading">{_icon_svg("💡", 24)}<span>AI Observation</span></h3>',
        unsafe_allow_html=True,
    )
    
    # Clean only the AI Observation content.
    raw_observation = str(summary.get("AI Observation", ""))

    # Remove HTML tags accidentally included in the observation text.
    raw_observation = re.sub(r"<[^>]*>", "", raw_observation)

    # Remove Markdown bold markers shown literally in the UI.
    raw_observation = raw_observation.replace("**", "")

    # Escape remaining content safely before inserting it into HTML.
    observation = html.escape(raw_observation.strip())
    observation = observation.replace("\n", "<br>")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(145deg, #151B35, #20183D);
            border: 1px solid rgba(139, 92, 246, 0.40);
            border-radius: 12px;
            padding: 14px 16px;
            color: #E2E8FF;
            line-height: 1.6;
            font-size: 14px;
            overflow-wrap: anywhere;
            white-space: normal;
            box-shadow: 0 4px 18px rgba(139, 92, 246, 0.10);
        ">{observation}</div>
        """,
        unsafe_allow_html=True,
    )



def detection_cards(object_counts, object_confidences, max_objects=None):
    """Render compact selectable object cards; selecting one reveals its statistics."""
    st.markdown(
        '<p class="neon-helper-text">Select an object to explore its detection statistics.</p>',
        unsafe_allow_html=True,
    )

    total_objects = sum(object_counts.values())
    if total_objects <= 0:
        st.caption("No detected objects to explore.")
        return

    sorted_objects = sorted(object_counts.items(), key=lambda item: item[1], reverse=True)
    if max_objects is not None:
        sorted_objects = sorted_objects[:max_objects]

    # Keep the selection in session state so the selected object's details remain visible.
    selected_key = "visionai_selected_detection_object"
    selected_obj = st.session_state.get(selected_key)

    with st.container(key="detection-explorer"):
        for obj, count in sorted_objects:
            scores = object_confidences.get(obj, [])
            if not scores:
                continue

            avg_conf = sum(scores) / len(scores)
            max_conf = max(scores)
            min_conf = min(scores)
            share = (count / total_objects) * 100
            obj_label = str(obj).title()
            is_selected = selected_obj == obj

            st.markdown(
                f'<div class="neon-object-caption">'
                f'<span class="neon-object-name">{_icon_svg("🎯", 18)}{html.escape(obj_label)}</span>'
                f'<span class="neon-object-meta">{count} detection{"s" if count != 1 else ""} '
                f'<span class="neon-dot">•</span> {share:.1f}% share</span></div>',
                unsafe_allow_html=True,
            )

            if st.button(
                "Hide statistics" if is_selected else "View statistics",
                key=f"select_detection_{str(obj)}",
                type="secondary",
            ):
                st.session_state[selected_key] = None if is_selected else obj
                st.rerun()

            if is_selected:
                row = st.columns(4)
                detail_cards = [
                    ("📦", "Count", count, "Total Detections"),
                    ("📈", "Average", f"{avg_conf * 100:.1f}%", "Avg Confidence"),
                    ("⬆️", "Highest", f"{max_conf * 100:.1f}%", "Highest Score"),
                    ("⬇️", "Lowest", f"{min_conf * 100:.1f}%", "Lowest Score"),
                ]
                for col, card in zip(row, detail_cards):
                    with col:
                        info_card(*card)
