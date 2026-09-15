import numpy as np
from scipy.stats import chi2

def portfolio_returns(price_matrix,weights):
    r=price_matrix.pct_change().dropna()
    common=[c for c in r.columns if c in weights.index]
    r=r[common].dropna()
    w=weights[common].astype(float); w=w/w.sum()
    return r.dot(w)

def historical_var(returns,confidence=.99):
    return float(-np.quantile(returns.dropna(),1-confidence))

def monte_carlo_var(returns,weights,paths=100000,confidence=.99,seed=42):
    returns=returns.dropna()
    w=weights.reindex(returns.columns).fillna(0.0); w=w/w.sum()
    mean=returns.mean().to_numpy()
    cov=returns.cov().to_numpy()+np.eye(len(mean))*1e-10
    L=np.linalg.cholesky(cov)
    rng=np.random.default_rng(seed)
    z=rng.standard_normal((paths,len(mean)))
    simulated=(z@L.T)+mean
    port=simulated@w.to_numpy()
    return float(-np.quantile(port,1-confidence)),port

def kupiec_test(breaches,observations,confidence=.99):
    p=1-confidence
    rate=breaches/observations
    def ll(x):
        x=min(max(x,1e-12),1-1e-12)
        return breaches*np.log(x)+(observations-breaches)*np.log(1-x)
    lr=-2*(ll(p)-ll(rate))
    return {"breaches":breaches,"observations":observations,
            "expected_rate":p,"observed_rate":rate,
            "lr_uc":float(lr),"p_value":float(chi2.sf(lr,1))}
