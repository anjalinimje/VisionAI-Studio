import streamlit as st
from pathlib import Path
import base64
import html




def _hero_image_data(filename: str, fallback: str) -> str:
    """Return an embeddable image URI; use an emoji if the asset is missing."""
    # hero.py is expected inside components/, with assets/ at project root.
    project_root = Path(__file__).resolve().parent.parent
    image_path = project_root / "assets" / "hero" / filename
    if image_path.is_file():
        suffix = image_path.suffix.lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(suffix, "image/png")
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f'<img src="data:{mime};base64,{encoded}" alt="{html.escape(filename.split(".")[0].title())}">'
    return f'<span class="hero-emoji" aria-label="{html.escape(filename.split(".")[0])}">{fallback}</span>'


def hero():


    left, right = st.columns([1.05, 0.95], gap="large")

    # =========================
    # LEFT SIDE
    # =========================

    with left:

        st.markdown(
            """
            <div class="hero-badge">
            ⚡ AI POWERED
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="title-white">See More.</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="title-gradient">Understand Everything.</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="hero-description">
            VisionAI Studio helps you detect, analyze and
            understand objects in images, videos and
            live streams with state-of-the-art YOLO models.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
        """, unsafe_allow_html=True)

        icon1, icon2, icon3, icon4 = st.columns([1, 1, 1, 1], gap="small")

        with icon1:
            st.markdown(
                    '<div class="mini-card"><i class="bi bi-bullseye feature-icon"></i></div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '<div class="mini-title">High Accuracy</div>',
                unsafe_allow_html=True
                
            )

            st.markdown(
                '<div class="mini-title">AI Models</div>',
                unsafe_allow_html=True
                
            )

        with icon2:
            st.markdown(
                '<div class="mini-card"><i class="bi bi-lightning-charge-fill feature-icon"></i></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Real Time</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Detection</div>',
                unsafe_allow_html=True
            )


        with icon3:
            st.markdown(
                '<div class="mini-card"><i class="bi bi-folder2-open feature-icon"></i></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Multiple</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Sources</div>',
                unsafe_allow_html=True
            )   


        with icon4:
            st.markdown(
                '<div class="mini-card"><i class="bi bi-bar-chart-line-fill feature-icon"></i></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Smart</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="mini-title">Analytics</div>',
                unsafe_allow_html=True
            )


        

    # =========================
    # RIGHT SIDE — use the complete hero artwork as one image
    # =========================
    with right:
        import streamlit.components.v1 as components

        hero_art = _hero_image_data("visionai_hero_frame.png", "")

        visual_html = f"""
        <!doctype html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            * {{ box-sizing: border-box; }}
            html, body {{
              margin: 0;
              padding: 0;
              width: 100%;
              background: transparent;
              overflow: hidden;
            }}
            .hero-artwork {{
              width: 100%;
              min-height: 330px;
              display: flex;
              align-items: center;
              justify-content: center;
              overflow: hidden;
            }}
            .hero-artwork img {{
              display: block;
              width: 100%;
              max-width: 680px;
              max-height: 470px;
              height: auto;
              object-fit: contain;
              object-position: center;
              filter: drop-shadow(0 10px 28px rgba(87, 38, 255, .18));
            }}
            @media (max-width: 700px) {{
              .hero-artwork {{ min-height: 260px; }}
              .hero-artwork img {{ max-height: 360px; }}
            }}
          </style>
        </head>
        <body>
          <div class="hero-artwork">
            {hero_art}
          </div>
        </body>
        </html>
        """
        components.html(visual_html, height=480, scrolling=False)


        # Performance / impact panel under the hero artwork
        st.markdown(
            """
            <div class="performance-impact-card" style="
                width:100%; margin-top:-160px; padding:14px 14px;
                display:flex; align-items:center; gap:14px;
                border:1px solid rgba(102,116,255,.25); border-radius:18px;
                background:linear-gradient(115deg, rgba(12,18,43,.96), rgba(16,13,44,.94) 58%, rgba(8,22,39,.96));
                box-shadow:0 12px 32px rgba(0,0,0,.20), inset 0 1px 0 rgba(150,130,255,.08);
                color:#eaf0ff; font-family:Inter, -apple-system, BlinkMacSystemFont, sans-serif;
                box-sizing:border-box; overflow:hidden;
            ">
              <div style="
                  flex:0 0 54px; width:54px; height:62px; display:flex;
                  align-items:center; justify-content:center; border-radius:15px;
                  background:radial-gradient(circle, rgba(63,126,255,.22), rgba(21,31,77,.08) 72%);
                  font-size:38px; filter:drop-shadow(0 0 13px rgba(70,115,255,.48));
              ">🏆</div>
              <div style="flex:1; min-width:0;">
                <div style="font-size:clamp(13px,1.15vw,17px); line-height:1.28; font-weight:750; letter-spacing:-.35px; margin-bottom:5px;">
                  Built for <span style="color:#31d9ff;">Performance.</span><br>
                  Designed for <span style="background:linear-gradient(90deg,#a47bff,#54bfff);-webkit-background-clip:text;background-clip:text;color:transparent;">Impact.</span>
                </div>
                <div style="font-size:11px; line-height:1.45; color:#aebbd5;">
                  Powerful computer vision, made intuitive for real-world workflows.
                </div>
              </div>
              <div style="
                  flex:0 0 40%; min-width:110px; padding-left:10px;
                  border-left:1px solid rgba(132,148,255,.20);
                  display:flex; flex-direction:column; gap:7px;
              ">
                <div style="display:flex; align-items:flex-start; gap:8px; color:#c8d3eb; font-size:10px; line-height:1.3;">
                  <span style="color:#4ce6f0;font-size:15px;line-height:1;">✓</span>
                  <span>State-of-the-art YOLO Models</span>
                </div>
                <div style="display:flex; align-items:flex-start; gap:8px; color:#c8d3eb; font-size:10px; line-height:1.3;">
                  <span style="color:#4ce6f0;font-size:15px;line-height:1;">✓</span>
                  <span>Fast &amp; Scalable Inference</span>
                </div>
                <div style="display:flex; align-items:flex-start; gap:8px; color:#c8d3eb; font-size:10px; line-height:1.3;">
                  <span style="color:#4ce6f0;font-size:15px;line-height:1;">✓</span>
                  <span>Export Reports &amp; Analytics</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


