import argparse,json,pandas as pd
from app.database import connect,load_price_matrix
from app.var_engine import portfolio_returns,historical_var,monte_carlo_var
from app.plotting import save_histogram

p=argparse.ArgumentParser(); p.add_argument("--db",default="data/market_data.db")
p.add_argument("--paths",type=int,default=100000); p.add_argument("--confidence",type=float,default=.99)
a=p.parse_args()
c=connect(a.db); prices=load_price_matrix(c)
w=pd.Series(1/prices.shape[1],index=prices.columns)
r=prices.pct_change().dropna(); port=portfolio_returns(prices,w)
h=historical_var(port,a.confidence); mc,_=monte_carlo_var(r,w,a.paths,a.confidence)
print(json.dumps({"assets":prices.shape[1],"price_rows":len(prices),
"return_observations":len(port),"confidence":a.confidence,
"historical_var":h,"monte_carlo_var":mc,"paths":a.paths},indent=2))
save_histogram(port,h)
