import sqlite3
from pathlib import Path
import pandas as pd

SCHEMA="""
CREATE TABLE IF NOT EXISTS prices(
 ticker TEXT NOT NULL, date TEXT NOT NULL, adjusted_close REAL NOT NULL,
 PRIMARY KEY(ticker,date));
CREATE TABLE IF NOT EXISTS portfolio_weights(
 ticker TEXT PRIMARY KEY, weight REAL NOT NULL);
"""
def connect(path="data/market_data.db"):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(path); c.executescript(SCHEMA); return c
def save_prices(c,df):
    df.to_sql("prices",c,if_exists="replace",index=False); c.commit()
def save_weights(c,df):
    df.to_sql("portfolio_weights",c,if_exists="replace",index=False); c.commit()
def load_price_matrix(c):
    df=pd.read_sql_query("select ticker,date,adjusted_close from prices",c)
    df["date"]=pd.to_datetime(df["date"])
    return df.pivot(index="date",columns="ticker",values="adjusted_close").sort_index()
