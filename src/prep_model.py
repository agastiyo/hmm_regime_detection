import pandas as pd
from utils.config import load_config

cfg = load_config()

df = pd.read_csv(cfg["data"]["processed_path"]).set_index("date")
returns = df[cfg["model"]["target_col"]].dropna()

# Splitting the data into training and testing sets to feed into the model
split_index = int(len(returns) * cfg["model"]["train_frac"])
train_data = returns[:split_index].values.reshape(-1, 1)
test_data = returns[split_index:].values.reshape(-1, 1)