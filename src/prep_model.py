import pandas as pd
from utils.config import load_config
from pathlib import Path

cfg = load_config()

df = pd.read_csv(cfg["data"]["processed_path"], parse_dates=["date"]).set_index("date")
returns = df[cfg["model"]["target_col"]]
symbol = cfg["data"]["symbol"]

# Splitting the data into a training set to feed into the model
split_index = int(len(returns) * cfg["model"]["train_frac"])
train_data = returns.iloc[:split_index].dropna()
full_data = returns.dropna()

# Saving the training data to CSV files
p = Path(f"data/temp/{symbol}/{symbol}_train_data.csv")
p.parent.mkdir(parents=True, exist_ok=True)
train_data.reset_index().to_csv(p, index=False)

p = Path(f"data/temp/{symbol}/{symbol}_full_data.csv")
p.parent.mkdir(parents=True, exist_ok=True)
full_data = full_data.reset_index().to_csv(p, index=False)