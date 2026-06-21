import streamlit as st
import pandas as pd
import pickle
import numpy as np

st.set_page_config(page_title="Gyrox Predictive Intelligence", layout="wide")
st.title("Gyrox Engine // Predictive Risk Dashboard")
st.subheader("Scope: Critical Minerals & Strategic Tech Export Controls")

try:
    # 1. Load trained model weights
    with open("gyrox_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # 2. Ingest the historical feature database
    df = pd.read_csv("feature_matrix.csv")
    latest_features = df.iloc[-1]
    
    # 3. Compute live probability score
    input_data = np.array([[latest_features['sentiment_score'], 
                            latest_features['mineral_spot_price'], 
                            latest_features['market_volume_deviations']]])
    prob_score = model.predict_proba(input_data)[0][1] * 100
    
    # 4. Display high-level metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="30-Day Export Restriction Probability", value=f"{prob_score:.2f}%")
    with col2:
        st.metric(label="US BIS Narrative Sentiment Score", value=f"{latest_features['sentiment_score']:.3f}")
    with col3:
        st.metric(label="Proxy Market Spot Price (SOXX)", value=f"${latest_features['mineral_spot_price']:.2f} USD")
        
    st.markdown("---")
    st.subheader("Historical Market Baseline Analytics (90-Day Horizon)")
    
    # 5. Build and project the interactive time-series chart
    chart_data = df.set_index('timestamp')[['mineral_spot_price']]
    st.line_chart(chart_data, y="mineral_spot_price", use_container_width=True)
    
    st.success("Gyrox Predictive engine operating with nominal local status.")

except FileNotFoundError:
    st.warning("Pipeline files missing. Please execute scripts in chronological sequence.")
