import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from pathlib import Path

DATA = Path("data/processed/flow_features.csv")
MODEL_OUT = Path("src/models/ids_iforest.joblib")

def main():
    df = pd.read_csv(DATA)

    features = df[
        ["connections", "unique_ports", "bytes_mean", "bytes_sum", "duration_mean"]
    ]

    model = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=42
    )

    model.fit(features)
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_OUT)

if __name__ == "__main__":
    main()
