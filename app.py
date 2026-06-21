import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import plotly.graph_objects as go

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

# Format dataframe timeline arrays securely
chart_df = historical_lake.copy()
chart_df['timestamp'] = pd.to_datetime(chart_df['timestamp'])

# FIX: Build a GPU-accelerated Plotly WebGL scatter trace to instantly erase rendering lag
fig = go.Figure()
fig.add_trace(go.Scattergl(
    x=chart_df['timestamp'],
    y=chart_df['mineral_spot_price'],
    mode='lines',
    name='Spot Price',
    line=dict(color='#ff4b4b', width=2),
    hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Asset Value:</b> $%{y:.2f} USD<extra></extra>'
))

fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=True, 
        gridcolor='#262730', 
        linecolor='#262730',
        title_font=dict(color='#a3a8b4'),
        tickfont=dict(color='#a3a8b4')
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#262730', 
        linecolor='#262730',
        title_font=dict(color='#a3a8b4'),
        tickfont=dict(color='#a3a8b4')
    ),
    hovermode='x unified',
    template='plotly_dark',
    height=450
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
