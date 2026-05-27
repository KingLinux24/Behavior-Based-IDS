from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import pandas as pd
from pathlib import Path

app = FastAPI(title="Behavior-Based IDS", version="1.0")

ALERTS_PATH = Path("data/processed/alerts.csv")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/alerts")
def get_alerts():
    if not ALERTS_PATH.exists():
        return {"message": "No alerts found. Run detection pipeline first."}
    df = pd.read_csv(ALERTS_PATH)
    return df.to_dict(orient="records")
