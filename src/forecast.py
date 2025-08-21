from run_model import model
from utils.config import load_config
import pandas as pd
import numpy as np
from pathlib import Path

cfg = load_config()
symbol = cfg["data"]["symbol"]  # Ticker symbol (e.g., 'QQQ')
returns = cfg["model"]["target_col"]  # Column name for returns
prices = cfg["data"]["price_col"]  # Column name for prices
n_steps = cfg["forecasting"]["n_steps"]  # Number of forecast steps
n_sims = cfg["forecasting"]["n_sims"]  # Number of Monte Carlo simulations per step


# Load the probabilities and states DataFrame and transition matrix
df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_probs_states.csv", parse_dates=["date"]).set_index("date")
transition_matrix_df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_transition_matrix.csv", index_col=0)
transition_matrix = transition_matrix_df.values  # 2x2 matrix for regime transitions


# Initialize the last known state probabilities (low and high volatility)
row = df.iloc[-1]
p_t = np.array([row["low_vol_prob"], row["high_vol_prob"]])
paths = [p_t.copy()]

# Start with the last known price; will be updated at each step
price_t = df[prices].iloc[-1]
# Store forecasted prices: [point_forecast, median_forecast, p05, p95]
price_paths = [np.array([price_t, np.nan, np.nan, np.nan])]

# Forecast loop: simulate future regime probabilities and prices
for i in range(n_steps):
  # Predict next step's regime probabilities
  p_next = paths[-1] @ transition_matrix
  paths.append(p_next)

  price_sims = []
  # Monte Carlo simulation for price at next step
  for j in range(n_sims):
    # Sample regime (0: low vol, 1: high vol) based on probabilities
    s = np.random.choice([0, 1], p=p_next)
    # Sample return from the regime's normal distribution
    r = np.random.normal(model.means_[s, 0], np.sqrt(model.covars_[s, 0]))
    # Calculate simulated price
    price_sims.append(price_t * np.exp(r))

  # Aggregate simulation results
  point_forecast = np.mean(price_sims)  # Mean forecast
  median_forecast = np.median(price_sims)  # Median forecast
  p05 = np.quantile(price_sims, 0.05)  # 5th percentile
  p95 = np.quantile(price_sims, 0.95)  # 95th percentile

  price_paths.append(np.array([point_forecast, median_forecast, p05, p95]))

  # Update price_t to the point forecast for the next step (compounding)
  price_t = point_forecast


# Create DataFrames for forecasted prices and regime probabilities
forecast_dates = pd.date_range(start=df.index[-1], periods=n_steps+1)
price_forecast_df = pd.DataFrame(price_paths, index=forecast_dates, columns=["point_forecast", "median_forecast", "p05", "p95"])
prob_forecast_df = pd.DataFrame(paths, index=forecast_dates, columns=["low_vol_prob", "high_vol_prob"])

# Combine into a single DataFrame
forecast_df = pd.concat([prob_forecast_df, price_forecast_df], axis=1)

# Save the forecasted prices and probabilities to CSV
p = Path(f"reports/{symbol}/tables/{symbol}_forecast.csv")
p.parent.mkdir(parents=True, exist_ok=True)
forecast_df.reset_index().to_csv(p, index=False)