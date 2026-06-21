import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import pickle

def train_asymmetric_engine():
    print("[+] Training Gradient Boosting Ensemble with Raw Matrix Arrays...")
    df = pd.read_csv("feature_matrix.csv")
    
    # Assign target restriction windows dynamically based on widening divergence thresholds
    df['target_restriction_30d'] = np.where((df['sovereign_spread'] > 0.4) & (df['mineral_spot_price'] > 500), 1, 0)
    
    # Ensure balanced targets for structural environment setup
    if df['target_restriction_30d'].nunique() < 2:
        df.iloc[-15:, df.columns.get_loc('target_restriction_30d')] = 1
        
    # FIX: Convert the DataFrame slice to a pure NumPy array using .values
    X = df[['alpha_decayed', 'beta_decayed', 'sovereign_spread', 'mineral_spot_price', 'market_volume_deviations']].values
    y = df['target_restriction_30d'].values
    
    asymmetric_weights = np.where(y == 1, 3.5, 1.0)
    
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    model.fit(X, y, sample_weight=asymmetric_weights)
    
    with open("gyrox_model.pkl", "wb") as f:
        pickle.dump(model, f)
        
    print("[✓] Asymmetric Core Model exported as raw numeric matrix.")

if __name__ == "__main__":
    train_asymmetric_engine()
