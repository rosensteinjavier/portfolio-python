from fastapi import FastAPI
from indicators import get_indicators
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}

def load_tickers():
    with open("tickers.txt") as f:
        return [l.strip() for l in f if l.strip()]

@app.get("/analyze")
def analyze():
    tickers = load_tickers()
    out = {}

    for t in tickers:
        try:
            out[t] = get_indicators(t)
        except Exception as e:
            out[t] = {"error": str(e)}

    return out

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
