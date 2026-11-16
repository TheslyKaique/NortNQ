"""Coletor de candles do NQ (Yahoo Finance) -> data.json

Uso:  python collector.py
Gera data.json na mesma pasta, com barras de 15 min em horário de Nova York (ET).
"""
import json, os, sys, tempfile
from datetime import datetime, timezone

import yfinance as yf

SYMBOL = "NQ=F"          # Nasdaq 100 futuro (NQ). MNQ usa os mesmos preços.
INTERVAL = "15m"
PERIOD = "5d"            # dá para cobrir pelo menos 2 pregões + madrugada
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def main():
    df = yf.download(SYMBOL, period=PERIOD, interval=INTERVAL, prepost=True,
                     auto_adjust=False, progress=False)
    if df is None or df.empty:
        sys.exit("Yahoo não devolveu candles; data.json anterior foi mantido.")
    if hasattr(df.columns, "levels"):          # versões novas do yfinance usam colunas multi-nível
        df.columns = df.columns.get_level_values(0)
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert("America/New_York")

    bars = []
    for ts, r in df.iterrows():
        bars.append([ts.strftime("%Y-%m-%d %H:%M"),
                     round(float(r["Open"]), 2), round(float(r["High"]), 2),
                     round(float(r["Low"]), 2), round(float(r["Close"]), 2),
                     int(r["Volume"]) if r["Volume"] == r["Volume"] else 0])

    if len({b[0][:10] for b in bars}) < 2:
        sys.exit("Menos de 2 dias de candles; data.json anterior foi mantido.")

    payload = {
        "symbol": SYMBOL,
        "source": "Yahoo Finance (NQ=F, atraso de cerca de 10 a 15 min)",
        "timezone": "America/New_York",
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bars": bars,
    }
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(OUT), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(",", ":"))
    os.replace(tmp, OUT)                        # escrita atômica
    print(f"{len(bars)} candles gravados em {OUT}")


if __name__ == "__main__":
    main()
