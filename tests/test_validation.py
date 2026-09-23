import pandas as pd
from app.validation import validate_prices
def test_clean():
    x=pd.DataFrame({"ticker":["A","A","B","B"],"date":["2024-01-01","2024-01-02"]*2,
                    "adjusted_close":[100,101,50,51]})
    assert validate_prices(x)["passed"] is True
def test_duplicate():
    x=pd.DataFrame({"ticker":["A","A"],"date":["2024-01-01"]*2,"adjusted_close":[100,100]})
    y=validate_prices(x)
    assert y["duplicate_rows"]==1 and y["passed"] is False
