from run_model import model
from utils.config import load_config
import pandas as pd
import numpy as np
from pathlib import Path

cfg = load_config()
symbol = cfg["data"]["symbol"]  # Ticker symbol (e.g., 'QQQ')
returns = cfg["model"]["target_col"]  # Column name for returns
prices = cfg["data"]["price_col"]  # Column name for prices
n_steps = cfg["forecasting"]["n_steps"]  # Number of days to forecast
n_sims = cfg["forecasting"]["n_sims"]  # Number of Monte Carlo simulations per step


# Load the probabilities and states DataFrame and transition matrix
df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_probs_states.csv", parse_dates=["date"]).set_index("date")
transition_matrix_df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_transition_matrix.csv", index_col=0)
transition_matrix = transition_matrix_df.values  # 2x2 matrix for regime transitions


# Initialize the last known state probabilities (low and high volatility)
row = df.iloc[-1]
p_t = np.array([row["low_vol_prob"], row["high_vol_prob"]])

# print(str(model.means_.shape) + " " + str(model.covars_.shape))

# --- Monte Carlo path simulation ---
last_price = df[prices].iloc[-1]
sim_prices = np.zeros((n_sims, n_steps + 1))
sim_prices[:, 0] = last_price

# For regime probabilities, keep a single path (mean) for reporting
regime_probs = [p_t.copy()]

for t in range(1, n_steps + 1):
  # Predict next step's regime probabilities (mean path)
  p_next = regime_probs[-1] @ transition_matrix
  regime_probs.append(p_next)

  # For each simulation, use its own previous price
  prev_prices = sim_prices[:, t-1]
  # Draw regimes for each simulation
  regimes = np.random.choice([0, 1], size=n_sims, p=p_next)
  # Draw returns for each simulation
  returns = np.random.normal(model.means_[regimes,0], np.sqrt(model.covars_[regimes,0,0]))
  # Update prices
  sim_prices[:, t] = prev_prices * np.exp(returns)

# Aggregate across all simulation paths for each step
price_paths = []
for t in range(n_steps + 1):
  point_forecast = np.mean(sim_prices[:, t])
  median_forecast = np.median(sim_prices[:, t])
  p05 = np.quantile(sim_prices[:, t], 0.05)
  p95 = np.quantile(sim_prices[:, t], 0.95)
  price_paths.append([point_forecast, median_forecast, p05, p95])

paths = regime_probs


# Create DataFrames for forecasted prices and regime probabilities
forecast_dates = pd.date_range(start=df.index[-1], periods=n_steps+1, freq='B')
price_forecast_df = pd.DataFrame(price_paths, index=forecast_dates, columns=["point_forecast", "median_forecast", "p05", "p95"])
prob_forecast_df = pd.DataFrame(paths, index=forecast_dates, columns=["low_vol_prob", "high_vol_prob"])

# Combine into a single DataFrame
forecast_df = pd.concat([prob_forecast_df, price_forecast_df], axis=1)

# Save the forecasted prices and probabilities to CSV
p = Path(f"reports/{symbol}/tables/{symbol}_forecast.csv")
p.parent.mkdir(parents=True, exist_ok=True)
forecast_df.reset_index().to_csv(p, index=False)