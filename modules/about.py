
import streamlit as st


def show_about_page():
    st.markdown("""
    <style>
    .about-panel {
        background: linear-gradient(135deg, #11132B, #0A0D1D);
        border: 1px solid rgba(139, 92, 246, 0.48);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0 20px 0;
        box-shadow:
            0 0 8px rgba(139, 92, 246, 0.12),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .about-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #22D3EE, #8B5CF6, #D946EF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .about-text {
        color: #C4CBE0;
        font-size: 15px;
        line-height: 1.8;
    }

    .step-card {
        height: 100%;
        min-height: 175px;
        background: linear-gradient(145deg, #15152F, #0D1124);
        border: 1px solid rgba(139, 92, 246, 0.42);
        border-radius: 13px;
        padding: 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .step-number {
        color: #22D3EE;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .step-heading {
        color: #F5F3FF;
        font-size: 18px;
        font-weight: 750;
        margin: 10px 0 8px 0;
    }

    .step-description {
        color: #B8C2DC;
        font-size: 14px;
        line-height: 1.6;
    }

    .about-tag {
        display: inline-block;
        color: #D8B4FE;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.35);
        padding: 6px 11px;
        border-radius: 20px;
        margin: 5px 5px 5px 0;
        font-size: 12px;
    }

    .workflow-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 20px;
        margin: 12px 0 22px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(15, 19, 42, 0.98), rgba(10, 13, 29, 0.98));
        border: 1px solid rgba(139, 92, 246, 0.32);
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.07), inset 0 1px 0 rgba(255,255,255,0.045);
        box-sizing: border-box;
        width: 100%;
    }

    .workflow-step {
        display: flex;
        align-items: flex-start;
        gap: 11px;
        min-width: 0;
    }

    .workflow-icon {
        width: 52px;
        height: 52px;
        min-width: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: linear-gradient(145deg, #14244B, #17112F);
        border: 1px solid rgba(65, 150, 255, 0.38);
        box-shadow: 0 0 10px rgba(40, 120, 255, 0.10),
                    inset 0 0 10px rgba(139, 92, 246, 0.08);
    }

    .workflow-icon svg {
        width: 27px;
        height: 27px;
        fill: none;
        stroke: #38CFFF;
        stroke-width: 1.8;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .workflow-heading {
        color: #F5F7FF;
        font-size: 15px;
        font-weight: 700;
        margin: 2px 0 6px;
    }

    .workflow-description {
        color: #AEBBD3;
        font-size: 12px;
        line-height: 1.55;
    }

    .workflow-arrow {
        color: #AFC0E3;
        font-size: 26px;
        line-height: 1;
        align-self: center;
        opacity: 0.9;
    }

    .about-tag {
        transition: transform 180ms ease, color 180ms ease,
                    background 180ms ease, border-color 180ms ease,
                    box-shadow 180ms ease;
        cursor: default;
        position: relative;
    }

    .about-tag:hover {
        color: #F3E8FF;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.28), rgba(34, 211, 238, 0.12));
        border-color: rgba(168, 85, 247, 0.82);
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.24),
                    inset 0 0 7px rgba(139, 92, 246, 0.08);
        transform: translateY(-2px);
    }

    .about-panel {
        transition: border-color 180ms ease, box-shadow 180ms ease;
    }

    .about-panel:hover {
        border-color: rgba(139, 92, 246, 0.62);
        box-shadow: 0 0 13px rgba(139, 92, 246, 0.10),
                    inset 0 1px 0 rgba(255,255,255,0.05);
    }

    @media (max-width: 1100px) {
        .workflow-container { flex-wrap: wrap; gap: 20px 14px; }
        .workflow-step { flex: 1 1 40%; }
        .workflow-arrow { display: none; }
    }

    @media (max-width: 700px) {
        .workflow-container { flex-direction: column; align-items: stretch; padding: 16px; gap: 18px; }
        .workflow-step { flex: 1 1 auto; align-items: center; }
        .workflow-description { font-size: 13px; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-panel">
        <div class="about-title">About VisionAI Studio</div>
        <div class="about-text">
            VisionAI Studio is a computer vision application designed to
            detect and analyze objects in images, videos, and live webcam
            streams using YOLO object detection models.
            <br><br>
            Its goal is to make object detection easier to explore through
            an intuitive interface, visual results, confidence scores,
            and analytics.
        </div>
        <br>
        <span class="about-tag">Computer Vision</span>
        <span class="about-tag">YOLO Models</span>
        <span class="about-tag">Real-Time Detection</span>
        <span class="about-tag">Visual Analytics</span>
    </div>
    """, unsafe_allow_html=True)

    

    
    st.markdown("""
<div style="margin: 8px 0 4px;">
<div class="about-title" style="font-size: 25px; margin-bottom: 4px;">How It Works</div>
<div class="about-text" style="font-size: 14px;">Follow these four steps to get started with VisionAI Studio.</div>
</div>
<div class="workflow-container">
<div class="workflow-step">
<div class="workflow-icon">
<svg viewBox="0 0 24 24">
<path d="M12 16V4"/>
<path d="M7 9l5-5 5 5"/>
<path d="M4 15v4a1 1 0 001 1h14a1 1 0 001-1v-4"/>
</svg>
</div>
<div>
<div class="workflow-heading">Upload</div>
<div class="workflow-description">
Upload an image, video<br>
or use your webcam
</div>
</div>
</div>
<div class="workflow-arrow">→</div>
<div class="workflow-step">
<div class="workflow-icon">
<svg viewBox="0 0 24 24">
<circle cx="12" cy="12" r="8"/>
<circle cx="12" cy="12" r="3"/>
<path d="M12 1v3M12 20v3M1 12h3M20 12h3"/>
</svg>
</div>
<div>
<div class="workflow-heading">Detect</div>
<div class="workflow-description">
AI model detects objects<br>
with high accuracy
</div>
</div>
</div>
<div class="workflow-arrow">→</div>
<div class="workflow-step">
<div class="workflow-icon">
<svg viewBox="0 0 24 24">
<path d="M4 19V10h4v9z"/>
<path d="M10 19V5h4v14z"/>
<path d="M16 19V2h4v17z"/>
<path d="M2 22h20"/>
</svg>
</div>
<div>
<div class="workflow-heading">Analyze</div>
<div class="workflow-description">
Get insights, confidence<br>
scores and analytics
</div>
</div>
</div>
<div class="workflow-arrow">→</div>
<div class="workflow-step">
<div class="workflow-icon">
<svg viewBox="0 0 24 24">
<path d="M12 3v12"/>
<path d="M7 10l5 5 5-5"/>
<path d="M4 17v4h16v-4"/>
</svg>
</div>
<div>
<div class="workflow-heading">Export</div>
<div class="workflow-description">
Download results, reports<br>
and share insights
</div>
</div>
</div>
</div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class="about-panel">
        <div class="about-title">Explore the Platform</div>
        <div class="about-text">
            <b>Image Detection</b> — detect objects in uploaded images.<br>
            <b>Video Detection</b> — analyze objects across video frames.<br>
            <b>Webcam Detection</b> — explore live camera detection.<br>
            <b>Dashboard & Analytics</b> — review the statistics available
            from your application.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Future Scope — added at the end; existing About page components remain unchanged.
    st.markdown("""    <div style="margin: 8px 0 4px;">
        <div class="about-title" style="font-size: 25px; margin-bottom: 4px;">
            <span style="display:inline-flex; align-items:center; justify-content:center;
                         width:34px; height:34px; margin-right:8px; vertical-align:middle;
                         border-radius:10px; background:linear-gradient(145deg,#14244B,#17112F);
                         border:1px solid rgba(139,92,246,.55);
                         box-shadow:0 0 12px rgba(139,92,246,.22);">
                <svg viewBox="0 0 24 24" width="20" height="20" style="vertical-align:middle;
                     fill:none; stroke:#38CFFF; stroke-width:1.8; stroke-linecap:round;
                     stroke-linejoin:round;">
                    <path d="M12 3v6"/><path d="M9 6l3-3 3 3"/>
                    <path d="M5 13a7 7 0 0 0 14 0"/>
                    <path d="M12 20v1"/>
                </svg>
            </span>
            Future Scope
        </div>
        <div class="about-text" style="font-size:14px;">
            Planned enhancements to expand VisionAI Studio's computer vision capabilities.
        </div>
    </div>
    <div class="future-scope-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;">
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <rect x="3" y="7" width="13" height="11" rx="2"/>
                    <path d="M16 11l5-3v9l-5-3"/>
                    <path d="M7 4h5"/>
                </svg>
            </div>
            <div class="step-heading">Object Tracking</div>
            <div class="step-description">Track detected objects across video frames and follow their movement.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <rect x="3" y="3" width="8" height="8" rx="1"/>
                    <rect x="13" y="3" width="8" height="8" rx="1"/>
                    <rect x="3" y="13" width="8" height="8" rx="1"/>
                    <rect x="13" y="13" width="8" height="8" rx="1"/>
                </svg>
            </div>
            <div class="step-heading">Instance Segmentation</div>
            <div class="step-description">Outline individual objects at pixel level for more detailed scene understanding.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <circle cx="12" cy="4" r="2"/>
                    <circle cx="6" cy="10" r="1.5"/>
                    <circle cx="18" cy="10" r="1.5"/>
                    <circle cx="8" cy="19" r="1.5"/>
                    <circle cx="16" cy="19" r="1.5"/>
                    <path d="M12 6v4M12 10l-6 0M12 10l6 0M12 10l-4 9M12 10l4 9"/>
                </svg>
            </div>
            <div class="step-heading">Pose Detection</div>
            <div class="step-description">Detect body keypoints and estimate human posture and movement.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <rect x="3" y="4" width="18" height="16" rx="2"/>
                    <path d="M7 9h2M11 9h1M15 9h2M7 13h10M7 16h7"/>
                </svg>
            </div>
            <div class="step-heading">OCR</div>
            <div class="step-description">Extract readable text from images, documents, and video frames.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <circle cx="12" cy="8" r="4"/>
                    <path d="M4 21a8 8 0 0 1 16 0"/>
                    <path d="M3 4v4M3 4h4M21 4v4M17 4h4"/>
                </svg>
            </div>
            <div class="step-heading">Face Detection</div>
            <div class="step-description">Locate faces in supported visual inputs, with privacy-aware handling.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <rect x="2" y="7" width="20" height="10" rx="2"/>
                    <path d="M5 7l2-3h10l2 3"/>
                    <circle cx="12" cy="12" r="2.5"/>
                </svg>
            </div>
            <div class="step-heading">License Plate Detection</div>
            <div class="step-description">Locate vehicle license plates and optionally extract plate text using OCR.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <path d="M3 3v18h18"/>
                    <path d="M7 15l4-5 4 3 5-7"/>
                    <circle cx="7" cy="15" r="1"/>
                    <circle cx="11" cy="10" r="1"/>
                    <circle cx="15" cy="13" r="1"/>
                    <circle cx="20" cy="6" r="1"/>
                </svg>
            </div>
            <div class="step-heading">Analytics Dashboard</div>
            <div class="step-description">Expand visual reports with trends, comparisons, and detection performance metrics.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <path d="M12 16V4"/>
                    <path d="M7 9l5-5 5 5"/>
                    <path d="M4 15v4a1 1 0 001 1h14a1 1 0 001-1v-4"/>
                </svg>
            </div>
            <div class="step-heading">Cloud Deployment</div>
            <div class="step-description">Deploy VisionAI Studio to cloud infrastructure for broader access and scaling.</div>
        </div>
        <div class="step-card" style="min-height:145px;">
            <div class="workflow-icon" style="width:52px;height:52px;min-width:52px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:linear-gradient(145deg,#14244B,#17112F);border:1px solid rgba(65,150,255,.55);box-shadow:0 0 14px rgba(56,207,255,.14),inset 0 0 12px rgba(139,92,246,.16);">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" stroke="#38CFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="display:block; flex-shrink:0;">
                    <path d="M10 13a5 5 0 0 0 7.1 0l2-2a5 5 0 0 0-7.1-7.1l-1.1 1.1"/>
                    <path d="M14 11a5 5 0 0 0-7.1 0l-2 2A5 5 0 0 0 12 20.1l1.1-1.1"/>
                </svg>
            </div>
            <div class="step-heading">API Support</div>
            <div class="step-description">Expose detection capabilities through APIs for integration with other applications.</div>
        </div>
    </div>
    <style>
        @media (max-width: 900px) {
            .future-scope-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            }
        }
        @media (max-width: 600px) {
            .future-scope-grid {
                grid-template-columns: 1fr !important;
            }
        }
    </style>""", unsafe_allow_html=True)
