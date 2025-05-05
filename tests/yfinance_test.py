import yfinance as yf
import pandas as pd
from datetime import datetime


stock_name = "BBAS3.SA"
ticker = yf.Ticker(stock_name)
history = ticker.history(period="1d")

if history.empty:
    raise ValueError(f"Não foi possível obter dados para o ticker {stock_name}")

preco_atual = history["Close"].iloc[-1]
info = ticker.info

lpa = info.get("trailingEps")
vpa = info.get("bookValue")

if lpa is None or vpa is None:
    raise ValueError(f"Dados insuficientes para {stock_name}: LPA ou VPA não disponíveis")

dividendos_history = ticker.dividends
dividendos_history.index = dividendos_history.index.tz_localize(None)

limite = pd.Timestamp.now() - pd.DateOffset(years=10)
dividendos_filtrados = dividendos_history[dividendos_history.index >= limite]

if dividendos_filtrados.empty:
    dpa_medio_anual = 0.0  
else:
    dividendos_anuais = dividendos_filtrados.groupby(dividendos_filtrados.index.year).sum()
    dpa_medio_anual = dividendos_anuais.mean().item()

print(preco_atual, lpa, vpa, dpa_medio_anual)