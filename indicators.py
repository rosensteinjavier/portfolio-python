import yfinance as yf
import pandas as pd

def to_float(x):

    try:
        return float(x.item())
    except:
        return float(x)

def get_indicators(ticker: str):
    data = yf.download(ticker, period="1y", interval="1d")

    data["EMA50"] = data["Close"].ewm(span=50).mean()
    data["EMA200"] = data["Close"].ewm(span=200).mean()

    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

    rs = gain / loss
    data["RSI"] = 100 - (100 / (1 + rs))

    latest = data.iloc[-1]

    return {
        "price": to_float(latest["Close"]),
        "rsi": to_float(latest["RSI"]),
        "ema50": to_float(latest["EMA50"]),
        "ema200": to_float(latest["EMA200"]),
    }

