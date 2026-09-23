import numpy as np,pandas as pd
from app.var_engine import historical_var,monte_carlo_var,kupiec_test
def test_historical_var_positive():
    assert historical_var(pd.Series([-.1,-.05,.01,.02,.03]),.8)>0
def test_mc_deterministic():
    r=pd.DataFrame(np.random.default_rng(1).normal(0,.01,(500,3)),columns=list("abc"))
    w=pd.Series([1/3]*3,index=list("abc"))
    v1,s1=monte_carlo_var(r,w,1000,seed=7); v2,s2=monte_carlo_var(r,w,1000,seed=7)
    assert v1==v2 and s1.shape==(1000,) and np.array_equal(s1,s2)
def test_kupiec():
    x=kupiec_test(0,1000,.99)
    assert x["lr_uc"]>=0 and 0<=x["p_value"]<=1
