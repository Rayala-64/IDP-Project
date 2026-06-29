import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Set page config as first Streamlit command
st.set_page_config(page_title="Dehazing Impact Dashboard", layout="wide")

# Ensure the project root is the working directory
PROJECT_ROOT = Path(__file__).parent
# Add the src directory to sys.path for module imports
sys.path.append(str(PROJECT_ROOT / "src"))
# Now import stopping_distance safely
# pyrefly: ignore [missing-import]
from evaluation import stopping_distance as sd

# Paths
RESULTS_ROOT = PROJECT_ROOT / "results"
SUMMARY_CSV = RESULTS_ROOT / "plots" / "summary.csv"
PLOTS_DIR = RESULTS_ROOT / "plots"
IMAGES_ROOT = RESULTS_ROOT
DETECTION_ROOT = RESULTS_ROOT

# Load summary data
@st.cache_data
def load_summary():
    if SUMMARY_CSV.exists():
        return pd.read_csv(SUMMARY_CSV)
    else:
        st.error(f"Summary CSV not found at {SUMMARY_CSV}")
        return pd.DataFrame()

summary_df = load_summary()

if not summary_df.empty:
    # Ensure PRI columns exist; compute if missing
    required = ["simple_pri", "dcp_pri"]
    missing = [col for col in required if col not in summary_df.columns]
    if missing:
        fog_yield = summary_df["fog_det"] * summary_df["fog_conf"]
        fog_yield = fog_yield.replace(0, pd.NA)
        if "simple_pri" in missing:
            simple_yield = summary_df["simple_det"] * summary_df["simple_conf"]
            summary_df["simple_pri"] = simple_yield / fog_yield
        if "dcp_pri" in missing:
            dcp_yield = summary_df["dcp_det"] * summary_df["dcp_conf"]
            summary_df["dcp_pri"] = dcp_yield / fog_yield
        summary_df["simple_pri"] = summary_df["simple_pri"].fillna(float('nan'))
        summary_df["dcp_pri"] = summary_df["dcp_pri"].fillna(float('nan'))

# Helper to retrieve image file paths for a given density and processing kind

def list_image_files(density: str, kind: str):
    """Return a list of image file Paths for the selected density and kind.
    kind can be 'original', 'simple', or 'full' corresponding to the subfolders.
    """
    kind_map = {
        "original": "foggy_outputs",
        "simple": "simple_dehazed_outputs",
        "full": "dcp_outputs",
    }
    folder = IMAGES_ROOT / density / "images" / kind_map.get(kind, "")
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])

# Helper to pick detection output image

def get_detection_image(density: str, kind: str, filename: str | None = None):
    kind_map = {
        "original": "foggy_outputs",
        "simple": "simple_dehazed_outputs",
        "full": "dcp_outputs",
    }
    folder = DETECTION_ROOT / density / "images" / kind_map.get(kind, "")
    if not folder.exists():
        return None
    imgs = sorted([p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    if filename:
        for img in imgs:
            if img.name == filename:
                return img
        return None
    return imgs[0] if imgs else None

# Styling – dark mode glass‑morphism with premium touches
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #0f0f1a, #1a1a2e); color: #cfcfcf; }
    .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 2rem; }
    .hero-text { font-size: 1.2rem; color: #a0a0c0; line-height: 1.6; }
    .kpi-card { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1.5rem; text-align: center; border-left: 4px solid #4a90e2; }
    .badge { padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: bold; }
    .bg-green { background: #2e7d32; }
    .bg-orange { background: #ef6c00; }
    .bg-red { background: #c62828; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==== Section 1 – Project Overview (Hero) ====
st.markdown("<div class='glass'><h1>Dehazing Impact Analysis</h1><p class='hero-text'>Evaluating the efficacy of Dark Channel Prior (DCP) algorithms in improving autonomous vehicle object detection under varying atmospheric obscuration.</p></div>", unsafe_allow_html=True)

# ==== Section 2 – Dataset Explorer (Compact) ====
st.subheader("Dataset Explorer")
col_density, col_type, col_image = st.columns([1, 1, 1.5])
with col_density:
    selected_density = st.selectbox(
        "Fog Density",
        options=["No_Fog", "Medium_Fog", "Dense_Fog"],
        index=0,
    )
with col_type:
    selected_kind = st.selectbox(
        "Image Type",
        options=["Original", "Simplified DCP", "Full DCP"],
        index=0,
    )
with col_image:
    kind_map_ui = {"Original": "original", "Simplified DCP": "simple", "Full DCP": "full"}
    current_kind = kind_map_ui[selected_kind]
    image_files = list_image_files(selected_density, current_kind)
    selected_image = None
    if image_files:
        file_names = [p.name for p in image_files]
        selected_name = st.selectbox("Sample Image", options=file_names)
        selected_image = next((p for p in image_files if p.name == selected_name), None)
    else:
        st.info("No images found for this selection.")

# ==== Section 3 – Dehazing Comparison ==== 
st.subheader("Dehazing Comparison")
if selected_image:
    col1, col2, col3 = st.columns(3)
    with col1:
        img_path = IMAGES_ROOT / selected_density / "images" / "foggy_outputs" / selected_image.name
        if img_path.exists():
            st.image(str(img_path), caption="Baseline: Obstructed View", width=400)
    with col2:
        img = get_detection_image(selected_density, "simple", selected_image.name)
        if img:
            st.image(str(img), caption="Simplified DCP: Contrast Enhancement", width=400)
        else:
            st.info("Simple DCP image not available.")
    with col3:
        img = get_detection_image(selected_density, "full", selected_image.name)
        if img:
            st.image(str(img), caption="Full DCP: Radiance Recovery", width=400)
        else:
            st.info("Full DCP image not available.")

# ==== Section 4 – Detection Comparison ==== 
st.subheader("Object Detection Comparison")
st.write("Visualizing the performance of YOLO-based detection pipelines across processed datasets.")

if selected_image:
    col1, col2, col3 = st.columns(3)
    with col1:
        img = get_detection_image(selected_density, "original", selected_image.name)
        if img:
            st.image(str(img), caption="Original Performance", width=400)
    with col2:
        img = get_detection_image(selected_density, "simple", selected_image.name)
        if img:
            st.image(str(img), caption="Simple DCP Detection", width=400)
    with col3:
        img = get_detection_image(selected_density, "full", selected_image.name)
        if img:
            st.image(str(img), caption="Full DCP Detection", width=400)

# ---- Detection Improvement Summary ----
st.subheader("Detection Improvement Summary")
if not summary_df.empty:
    df_sel = summary_df[summary_df["density"] == selected_density]
    if not df_sel.empty:
        row = df_sel.iloc[0]
        fog_det = row.get("fog_det", float('nan'))
        dcp_det = row.get("dcp_det", float('nan'))
        dcp_pri = row.get("dcp_pri", float('nan'))
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric(label="Fog Detection Count", value=f"{fog_det:.1f}")
        with col_b:
            st.metric(label="Full DCP Count", value=f"{dcp_det:.1f}")
        with col_c:
            st.metric(label="Full DCP PRI", value=f"{dcp_pri:.2f}")
        st.caption(f"Full DCP achieved a PRI of {dcp_pri:.2f}, indicating improved perception effectiveness relative to the foggy baseline.")
    else:
        st.info("No metric data for selected density.")
else:
    st.info("Summary data unavailable.")

# ==== Section 5 – Object Detection Analysis (Plots) ==== 
st.subheader("Object Detection Analysis")
plot_cols = st.columns(2)
with plot_cols[0]:
    detection_img = PLOTS_DIR / "detection.png"
    if detection_img.exists():
        st.image(str(detection_img), caption="Quantitative Count Analysis")
with plot_cols[1]:
    confidence_img = PLOTS_DIR / "confidence.png"
    if confidence_img.exists():
        st.image(str(confidence_img), caption="Detection Confidence Distribution")

# ==== Section 6 – Quantitative Comparison ==== 
st.subheader("Quantitative Comparison")
if not summary_df.empty:
    df = summary_df[summary_df["density"] == selected_density]
    if not df.empty:
        base_cols = ["fog_det", "simple_det", "dcp_det", "fog_conf", "simple_conf", "dcp_conf"]
        pri_cols = []
        if "simple_pri" in df.columns:
            pri_cols.append("simple_pri")
        if "dcp_pri" in df.columns:
            pri_cols.append("dcp_pri")
        cols = base_cols + pri_cols
        display_df = df[cols]
        rename_map = {
            "fog_det": "Fog Count",
            "simple_det": "Simple Count",
            "dcp_det": "Full DCP Count",
            "fog_conf": "Fog Avg Conf",
            "simple_conf": "Simple Avg Conf",
            "dcp_conf": "Full DCP Avg Conf",
        }
        if "simple_pri" in pri_cols:
            rename_map["simple_pri"] = "Simple PRI"
        if "dcp_pri" in pri_cols:
            rename_map["dcp_pri"] = "Full DCP PRI"
        display_df = display_df.rename(columns=rename_map).round(3)
        styled = display_df.style.format('{:.3f}').set_properties(**{'text-align': 'center'}).background_gradient(cmap='Blues')
        st.dataframe(styled)
    else:
        st.info("No metrics available for selected density.")
else:
    st.info("No summary data to display.")

# ==== Section 7 – Perception Analysis (KPI cards) ====
st.subheader("Perception Analysis")
if not summary_df.empty:
    selected_row = summary_df[summary_df["density"] == selected_density]
    if not selected_row.empty:
        row = selected_row.iloc[0]
        avg_det = row.get("dcp_det", float('nan'))
        avg_conf = row.get("dcp_conf", float('nan'))
        avg_pri = row.get("dcp_pri", float('nan'))
    else:
        avg_det = avg_conf = avg_pri = float('nan')
    def interp(pri):
        if pd.isna(pri): return "N/A"
        if pri < 1.0: return "Degradation"
        if pri < 1.5: return "Minimal Recovery"
        if pri < 3.0: return "Moderate Recovery"
        return "Strong Recovery"
    interpretation = interp(avg_pri)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='kpi-card'><h4>Detection Yield</h4><p style='font-size: 2rem;'>{avg_det:.2f}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi-card'><h4>Confidence Index</h4><p style='font-size: 2rem;'>{avg_conf:.2f}</p></div>", unsafe_allow_html=True)
    with col3:
        color = "green" if avg_pri >= 1.5 else "red"
        st.markdown(f"<div class='kpi-card'><h4>Perception Impact (PRI)</h4><p style='font-size: 2rem; color:{color};'>{avg_pri:.2f}</p><small>{interpretation}</small></div>", unsafe_allow_html=True)
else:
    st.info("KPI data unavailable.")

# ==== Section 8 – Transportation Safety Assessment ====
st.subheader("Transportation Safety Assessment")
if not summary_df.empty:
    row = summary_df[summary_df["density"] == selected_density]
    if not row.empty:
        pri_val = row.iloc[0]["dcp_pri"]
        safety = sd.summarize(selected_density, detection_count=0, avg_confidence=0, pri=pri_val)
        col1, col2, col3 = st.columns(3)
        with col1:
            level = safety["risk"].upper()
            c = "bg-green" if level == "LOW" else "bg-orange" if level == "MODERATE" else "bg-red"
            st.markdown(f"<div class='kpi-card'><h4>Risk Level</h4><br><span class='badge {c}'>{level}</span></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='kpi-card'><h4>Safe Velocity</h4><br><p style='font-size: 1.5rem;'>{safety['speed']} km/h</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='kpi-card'><h4>Stopping Distance</h4><br><p style='font-size: 1.5rem;'>{safety['stopping_distance']:.1f} m</p></div>", unsafe_allow_html=True)
        st.markdown(f"**Research Summary**: {safety['text']}")
    else:
        st.info("No data for selected density.")
else:
    st.info("Safety assessment unavailable due to missing summary.")

# ==== Section 9 – Project Insight (Final Highlight) ====
st.subheader("Project Insight")
st.markdown(
    """
    <div class='glass' style='text-align:center;'>
    <p style='font-size:1.1rem;'>This work demonstrates how image dehazing influences downstream object detection under foggy driving conditions.</p>
    <p style='font-size:1rem;'>The proposed Perception Recovery Index (PRI) combines detection yield and confidence into a single perception effectiveness measure.</p>
    <p style='font-size:1rem;'>A transportation safety layer translates perception quality into actionable driving recommendations including risk level, speed, and stopping distance.</p>
    <div style='display:flex; justify-content:center; align-items:center; gap:12px; margin-top:0.6rem;'>
        <span>🌫️ Fog</span> → <span>🔍 Dehazing</span> → <span>🎯 Detection</span> → <span>🧠 PRI</span> → <span>🚦 Safety</span>
    </div>
    </div>
    """,
    unsafe_allow_html=True)

# End of dashboard
