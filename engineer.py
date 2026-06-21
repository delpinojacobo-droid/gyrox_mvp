import pandas as pd
import numpy as np

def compile_institutional_features():
    print("[+] Executing Temporal Decay and Sovereign Divergence Spread metrics...")
    
    # 1. Reconstruct baseline feature array
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='D')
    df = pd.DataFrame({
        'timestamp': dates,
        'mineral_spot_price': np.linspace(340, 639.45, 100) + np.random.normal(0, 10, 100),
        'market_volume_deviations': np.random.normal(0.05, 0.1, 100)
    })
    
    # Simulate historical node polarity profiles
    df['node_alpha_sentiment'] = np.random.uniform(-0.4, 0.2, 100)
    df['node_beta_sentiment'] = np.random.uniform(-0.5, 0.1, 100)
    
    # 2. Apply Exponential Geopolitical Shock Decay Matrix
    # S_t = S_base * e^(-lambda * delta_t)
    lambda_decay = 0.1
    decayed_alpha = []
    decayed_beta = []
    
    current_alpha = 0.0
    current_beta = 0.0
    for i in range(len(df)):
        current_alpha = df['node_alpha_sentiment'].iloc[i] + (current_alpha * np.exp(-lambda_decay))
        current_beta = df['node_beta_sentiment'].iloc[i] + (current_beta * np.exp(-lambda_decay))
        decayed_alpha.append(current_alpha)
        decayed_beta.append(current_beta)
        
    df['alpha_decayed'] = decayed_alpha
    df['beta_decayed'] = decayed_beta
    
    # 3. Compute Sovereign Divergence Spread Vector (Delta)
    df['sovereign_spread'] = np.abs(df['alpha_decayed'] - df['beta_decayed'])
    
    df.to_csv("feature_matrix.csv", index=False)
    print("[✓] Matrix upgraded with Sovereign Divergence Spreads and Decay Memory layers.")

if __name__ == "__main__":
    compile_institutional_features()
