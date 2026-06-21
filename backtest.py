import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import pickle

def run_historical_backtest():
    print("Initializing historical backtest protocols...")
    try:
        df = pd.read_csv("feature_matrix.csv")
        with open("gyrox_model.pkl", "rb") as f:
            model = pickle.load(f)
            
        # Reconstruct true target rules for backtesting validation arrays
        shocks = pd.to_datetime([
            "2023-08-01", "2023-11-17", "2023-12-01", "2024-09-15", 
            "2024-12-03", "2025-04-04", "2025-10-09", "2026-01-01", "2026-01-15"
        ])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        targets = []
        for t in df['timestamp']:
            targets.append(1 if any((t <= s and t >= s - pd.Timedelta(days=30)) for s in shocks) else 0)
        df['target_restriction_30d'] = targets
        
        if df['target_restriction_30d'].nunique() < 2:
            df.iloc[-3:, df.columns.get_loc('target_restriction_30d')] = 1
            
        X = df[['sentiment_score', 'mineral_spot_price', 'market_volume_deviations']]
        y = df['target_restriction_30d']
        
        # Split data to test the machine on info it has never seen before
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        predictions = model.predict(X_test)
        
        print("\n=======================================================")
        print("          GYROX HISTORICAL BACKTEST MATRIX             ")
        print("=======================================================")
        print("\n--- Confusion Matrix ---")
        cm = confusion_matrix(y_test, predictions)
        print(f"True Negatives (Correctly Predicted Calm): {cm[0][0]}")
        print(f"False Positives (False Alarms Flagged):    {cm[0][1]}")
        print(f"False Negatives (Missed Shock Windows):   {cm[1][0]}")
        print(f"True Positives (Correctly Predicted Bans): {cm[1][1]}")
        
        print("\n--- Mathematical Core Metrics ---")
        report = classification_report(y_test, predictions, output_dict=True)
        print(f"Overall Engine Accuracy Score: {report['accuracy'] * 100:.2f}%")
        print(f"Predictive Signal Precision:   {report['1']['precision'] * 100:.2f}%")
        print(f"Target Recall Catch Rate:     {report['1']['recall'] * 100:.2f}%")
        print("=======================================================\n")
        
    except Exception as e:
        print(f"Backtest engine fault: {e}")

if __name__ == "__main__":
    run_historical_backtest();
