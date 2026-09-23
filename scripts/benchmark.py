import argparse,time,numpy as np,pandas as pd
from app.var_engine import monte_carlo_var
p=argparse.ArgumentParser(); p.add_argument("--paths",type=int,default=100000); a=p.parse_args()
rng=np.random.default_rng(42); r=pd.DataFrame(rng.normal(0,.01,(1000,30)))
w=pd.Series(np.ones(30)/30)
t=time.perf_counter(); monte_carlo_var(r,w,a.paths,seed=42); elapsed=time.perf_counter()-t
print(f"Vectorized Monte Carlo: {a.paths:,} paths in {elapsed:.3f}s")
