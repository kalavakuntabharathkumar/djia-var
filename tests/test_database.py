import pandas as pd
from app.database import connect,save_prices,load_price_matrix
def test_round_trip(tmp_path):
    c=connect(str(tmp_path/"x.db"))
    x=pd.DataFrame({"ticker":["A","A","B","B"],
                    "date":pd.to_datetime(["2024-01-01","2024-01-02"]*2),
                    "adjusted_close":[100,101,50,51]})
    save_prices(c,x); m=load_price_matrix(c)
    assert m.shape==(2,2) and m.loc[pd.Timestamp("2024-01-02"),"A"]==101
