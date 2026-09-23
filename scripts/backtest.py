import argparse,json,pandas as pd
from app.database import connect,load_price_matrix
from app.var_engine import portfolio_returns,historical_var,kupiec_test

p=argparse.ArgumentParser(); p.add_argument("--db",default="data/market_data.db")
p.add_argument("--window",type=int,default=1000); p.add_argument("--days",type=int,default=1250)
p.add_argument("--confidence",type=float,default=.99); a=p.parse_args()
prices=load_price_matrix(connect(a.db)); w=pd.Series(1/prices.shape[1],index=prices.columns)
r=portfolio_returns(prices,w)
if len(r)<a.window+a.days: raise RuntimeError("Not enough observations")
test=r.iloc[-a.days:]; history=r.iloc[:-a.days]
breaches=0; rows=[]
for i,(date,realized) in enumerate(test.items()):
    rolling=pd.concat([history.iloc[max(0,len(history)-a.window+i):],test.iloc[:i]])
    var=historical_var(rolling,a.confidence); breach=float(realized)<-var
    breaches+=int(breach); rows.append({"date":date,"realized_return":float(realized),"var":var,"breach":breach})
result=kupiec_test(breaches,len(test),a.confidence); print(json.dumps(result,indent=2))
pd.DataFrame(rows).to_csv("reports/var_backtest.csv",index=False)
