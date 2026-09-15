import argparse,time
import pandas as pd
import yfinance as yf
from app.database import connect,save_prices,save_weights
from app.tickers import DOW_30
from app.validation import validate_prices

def run(years,db):
    end=pd.Timestamp.utcnow().tz_localize(None).normalize()
    start=end-pd.DateOffset(years=years)
    rows=[]
    for ticker in DOW_30:
        print("Downloading",ticker)
        raw=yf.download(ticker,start=start.strftime("%Y-%m-%d"),
                         end=(end+pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
                         auto_adjust=False,progress=False)
        if raw.empty: continue
        if isinstance(raw.columns,pd.MultiIndex):
            s=raw[("Adj Close",ticker)] if ("Adj Close",ticker) in raw.columns else raw["Adj Close"].iloc[:,0]
        else: s=raw["Adj Close"]
        x=s.rename("adjusted_close").reset_index()
        x.columns=["date","adjusted_close"]; x["ticker"]=ticker
        rows.append(x[["ticker","date","adjusted_close"]]); time.sleep(.1)
    if not rows: raise RuntimeError("No market data downloaded")
    prices=pd.concat(rows,ignore_index=True)
    prices["date"]=pd.to_datetime(prices["date"]).dt.tz_localize(None)
    print(validate_prices(prices))
    c=connect(db); save_prices(c,prices)
    save_weights(c,pd.DataFrame({"ticker":DOW_30,"weight":[1/30]*30})); c.close()
    print("Saved",len(prices),"rows to",db)

if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--years",type=int,default=10)
    p.add_argument("--db",default="data/market_data.db"); a=p.parse_args(); run(a.years,a.db)
