import json
import pandas as pd
from pathlib import Path

IN_PATH = Path("data/raw/flows.jsonl")
OUT_PATH = Path("data/processed/flow_features.csv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def main():
    rows = []
    with IN_PATH.open("r") as f:
        for line in f:
            rows.append(json.loads(line))

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["window"] = df["timestamp"].dt.floor("1min")

    grouped = df.groupby(["host", "src_ip", "window"]).agg(
        connections=("dst_port", "count"),
        unique_ports=("dst_port", "nunique"),
        bytes_mean=("bytes", "mean"),
        bytes_sum=("bytes", "sum"),
        duration_mean=("duration", "mean"),
    ).reset_index()

    grouped.to_csv(OUT_PATH, index=False)

if __name__ == "__main__":
    main()
