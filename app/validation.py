import pandas as pd
def validate_prices(df):
    req={"ticker","date","adjusted_close"}
    if req-set(df.columns): raise ValueError(f"Missing columns: {sorted(req-set(df.columns))}")
    x=df.copy(); x["date"]=pd.to_datetime(x["date"])
    duplicates=int(x.duplicated(["ticker","date"]).sum())
    nonpositive=int((x.adjusted_close<=0).sum())
    gaps={}
    for t,g in x.groupby("ticker"):
        d=pd.DatetimeIndex(sorted(g.date.unique()))
        if len(d)>1:
            gaps[t]=int(len(pd.date_range(d.min(),d.max(),freq="B").difference(d)))
    y=x.sort_values(["ticker","date"]).copy()
    y["return"]=y.groupby("ticker").adjusted_close.pct_change()
    jumps=int((y["return"].abs()>.50).sum())
    return {"rows":len(x),"tickers":x.ticker.nunique(),"duplicate_rows":duplicates,
            "non_positive_prices":nonpositive,"gap_counts":gaps,
            "suspicious_moves_over_50pct":jumps,
            "passed":duplicates==0 and nonpositive==0}
