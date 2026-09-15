from pathlib import Path
import matplotlib.pyplot as plt
def save_histogram(returns,var,path="reports/return_distribution.png"):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    plt.figure(figsize=(9,5))
    plt.hist(returns,bins=80)
    plt.axvline(-var,linestyle="--",label=f"VaR={-var:.4f}")
    plt.title("Portfolio Daily Return Distribution")
    plt.xlabel("Daily return"); plt.ylabel("Frequency"); plt.legend()
    plt.tight_layout(); plt.savefig(path,dpi=150); plt.close()
