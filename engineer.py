import pandas as pd
from transformers import pipeline
import yfinance as yf
from datetime import datetime, timedelta

def analyze_and_merge():
    print("Processing language sentiment...")
    df = pd.read_csv("raw_narratives.csv")
    nlp = pipeline("sentiment-analysis", model="DistilBERT-base-uncased-finetuned-sst-2-english")
    
    scores = []
    for text in df['headline']:
        res = nlp(text)[0]
        scores.append(res['score'] if res['label'] == 'POSITIVE' else -res['score'])
        
    df['sentiment_score'] = scores
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
    daily = df.groupby('timestamp')['sentiment_score'].mean().reset_index()
    
    print("Pulling live market data for SOXX...")
    start = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')
    mkt = yf.download("SOXX", start=start).reset_index()
    
    if isinstance(mkt.columns, pd.MultiIndex):
        mkt.columns = [c[0] for c in mkt.columns]
        
    mkt['Date'] = pd.to_datetime(mkt['Date']).dt.tz_localize(None)
    mkt = mkt[['Date', 'Close', 'Volume']]
    mkt.columns = ['timestamp', 'mineral_spot_price', 'market_volume_deviations']
    
    final = pd.merge(mkt, daily, on='timestamp', how='left').fillna(0.0)
    v_mean = final['market_volume_deviations'].mean()
    final['market_volume_deviations'] = (final['market_volume_deviations'] - v_mean) / v_mean
    
    final.to_csv("feature_matrix.csv", index=False)
    print("Feature engineering complete. Live data matrix saved.")

if __name__ == "__main__":
    analyze_and_merge()
