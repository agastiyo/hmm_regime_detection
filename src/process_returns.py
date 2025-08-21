import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from utils.config import load_config

cfg = load_config()

def main():
  df = load_prices(cfg["data"]["raw_path"])
  df = compute_returns(df, price=cfg["data"]["price_col"])
  save_processed(df, cfg["data"]["processed_path"])

# Loads the raw pricing data, parses dates into datetime, and forces all numerical values to be integers
def load_prices(in_path):
  df = pd.read_csv(in_path, parse_dates=["date"])
  
  df.columns = [c.strip().lower() for c in df.columns]
  df = df.sort_values("date").set_index("date")
  
  df = df[~df.index.duplicated(keep='first')]
  df = df.drop_duplicates()
  
  # Convert all columns except 'date' to numeric
  numeric_cols = [c for c in df.columns if c != "date"]
  df = df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
  
  # Replace empty strings with NaN
  df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
  # Drop rows where all columns are NaN
  df.dropna(how='all', inplace=True)
  
  # Remove all times before 2000-03-20
  df = df.loc[df.index > pd.Timestamp("2000-03-20")]
  
  return df

# Computes the simple and log close-to-close returns and adds the to the data frame
def compute_returns(df,price="adj_close"):
  if price not in df.columns:
    raise KeyError(f"Price column '{price}' not found.")
  
  px = df[price].astype(float)
  prev = px.shift(1)
  
  df["simple_ret"] = (px / prev) - 1.0
  
  ratio = (px / prev).where((px > 0) & (prev > 0))
  df["log_ret"] = np.log(ratio)
  
  return df

# Saves the processed data
def save_processed(df,out_path):
  p = Path(out_path)
  p.parent.mkdir(parents=True, exist_ok=True)
  df.reset_index().to_csv(p, index=False)
  
if __name__ == "__main__":
  main()