import argparse
from pathlib import Path
import numpy as np
import pandas as pd

global df

# Loads the raw pricing data, parses dates into datetime, and forces all numerical values to be integers
def load_prices(in_path):
  df = pd.read_csv(in_path, parse_dates=["date"])
  
  df.columns = [c.strip().lower() for c in df.columns]
  df = df.sort_values("date").set_index("date")
  
  numeric_cols = [c for c in df.columns if c != "date"]
  df = df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
  
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

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--in_path", required=True, help="Input CSV with columns incl. date, adj_close")
  ap.add_argument("--out_path", required=True, help="Output CSV with returns")
  ap.add_argument("--price", default="adj_close", help="Price column to use (default: adj_close)")
  args = ap.parse_args()
  
  df = load_prices(args.in_path)
  df = compute_returns(df, price=args.price)
  save_processed(df, args.out_path)
  
if __name__ == "__main__":
  main()
  
# To Run in terminal:
# python3 -m src.returns --in_path [PATH HERE] --out_path [PATH HERE]
# Make sure the csv you input has a date and adj_close column