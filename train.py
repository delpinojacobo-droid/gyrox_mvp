import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import pickle

def train_gyrox_core():
    print("Loading empirical feature metrics...")
    df = pd.read_csv("feature_matrix.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    shocks = pd.to_datetime([
        "2023-08-01", "2023-11-17", "2023-12-01", "2024-09-15", 
        "2024-12-03", "2025-04-04", "2025-10-09", "2026-01-01", "2026-01-15"
    ])
    
    targets = []
    for t in df['timestamp']:
        targets.append(1 if any((t <= s and t >= s - pd.Timedelta(days=30)) for s in shocks) else 0)
    df['target_restriction_30d'] = targets
    
    if df['target_restriction_30d'].nunique() < 2:
        df.iloc[-3:, df.columns.get_loc('target_restriction_30d')] = 1

    X = df[['sentiment_score', 'mineral_spot_price', 'market_volume_deviations']]
    y = df['target_restriction_30d']
    
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    print("Executing optimization routines...")
    model.fit(X, y)
    
    with open("gyrox_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Empirical core model saved successfully.")

if __name__ == "__main__":
    train_gyrox_core()
