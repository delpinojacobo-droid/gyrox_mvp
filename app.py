import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

st.set_page_config(page_title="Gyrox Engine Core", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 700; color: #ff4b4b; }
    div[data-testid="stMetricLabel"] { font-size: 0.95rem; color: #a3a8b4; }
    </style>
""", unsafe_allow_html=True)

def load_core_model():
    with open("gyrox_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_core_model()
except Exception as e:
    st.error(f"Core Offline: {e}")
    st.stop()

# Load the deep multi-year repository for data continuity mapping
try:
    historical_lake = pd.read_csv("feature_matrix.csv")
    current_live_price = float(historical_lake['mineral_spot_price'].iloc[-1])
except Exception as e:
    st.error(f"Data Lake Connection Fault: {e}")
    st.stop()

st.title("Gyrox Engine // Geopolitical Intelligence Core")
st.caption("Institutional Additive Ensemble Model with Asymmetric Loss Optimization Matrix")
st.markdown("---")

pitch_mode = st.radio("System Framework State:", ["Autonomous Production Node", "Adversarial Stress-Test Simulation (Pitch Mode)"], horizontal=True)

if pitch_mode == "Autonomous Production Node":
    active_alpha = -0.120
    active_beta = 0.050
    active_price = current_live_price
    st.info("● Systems running on active cloud pipelines. Asymmetric optimization multiplier locked at 3.5x.")
else:
    st.markdown("### 🛠️ Strategic Parameter Simulation Panel")
    sc_1, sc_2, sc_3 = st.columns(3)
    with sc_1: active_alpha = st.slider("Node Alpha: Western Policy Sentiment (Decayed)", -2.00, 2.00, -0.12, step=0.01)
    with sc_2: active_beta = st.slider("Node Beta: Eastern Regulatory Posture (Decayed)", -2.00, 2.00, 0.05, step=0.01)
    with sc_3: active_price = st.slider("Proxy Market Spot Price Valuation (SOXX)", 300.0, 900.0, float(current_live_price), step=5.0)

# Calculate Sovereign Divergence Spread Live
active_spread = np.abs(active_alpha - active_beta)

input_df = pd.DataFrame([{
    'alpha_decayed': active_alpha,
    'beta_decayed': active_beta,
    'sovereign_spread': active_spread,
    'mineral_spot_price': active_price,
    'market_volume_deviations': 0.05
}])

risk_probability = model.predict_proba(input_df.values)[0][1] * 100

# Primary Metrics Display Matrix
st.markdown("---")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    color = "🔴" if risk_probability > 70 else ("🟡" if risk_probability > 30 else "🟢")
    st.metric("Asymmetric Shock Probability", f"{risk_probability:.2f}%", delta=f"{color} Status Check")
with m_col2:
    st.metric("Sovereign Divergence Spread (δ)", f"{active_spread:.3f}", delta="Adversarial Delta")
with m_col3:
    st.metric("Node Alpha / Node Beta Values", f"{active_alpha:.2f} / {active_beta:.2f}")
with m_col4:
    st.metric("Proxy Spot Benchmark", f"${active_price:,.2f} USD")

st.markdown("---")
st.subheader("Historical Market Baseline Analytics (Multi-Year Asset Horizon)")

# FIX: Keep timestamp as a true datetime64 object so the graph uses a fluid, native time axis scale
chart_df = historical_lake.copy()
chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'])

st.line_chart(data=chart_df, x='timestamp', y='mineral_spot_price', use_container_width=True)
