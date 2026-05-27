import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = Path("src/models/ids_iforest.joblib")
DATA = Path("data/processed/flow_features.csv")
OUT = Path("data/processed/alerts.csv")

def main():
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA)

    features = df[
        ["connections", "unique_ports", "bytes_mean", "bytes_sum", "duration_mean"]
    ]

    scores = model.decision_function(features)
    preds = model.predict(features)

    df["anomaly_score"] = scores
    df["anomaly"] = (preds == -1)

    alerts = df[df["anomaly"]].sort_values("anomaly_score")
    alerts.to_csv(OUT, index=False)

if __name__ == "__main__":
    main()
