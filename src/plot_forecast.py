import pandas as pd
import matplotlib.pyplot as plt
from utils.config import load_config
from pathlib import Path

cfg = load_config()
symbol = cfg["data"]["symbol"]
price_col = cfg["data"]["price_col"]
n_steps = cfg["forecasting"]["n_steps"]

# Load historical prices
hist_df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_probs_states.csv", parse_dates=["date"]).set_index("date")

# Load forecast
forecast_df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_forecast.csv", parse_dates=["index"]).set_index("index")

# Plot
plt.figure(figsize=(14, 7))
plt.plot(hist_df.index, hist_df[price_col], label="Historical Price", color="black")
plt.plot(forecast_df.index, forecast_df["point_forecast"], label="Forecast (mean)", color="blue")
plt.plot(forecast_df.index, forecast_df["median_forecast"], label="Forecast (median)", color="orange", linestyle="--")
plt.fill_between(forecast_df.index, forecast_df["p05"], forecast_df["p95"], color="blue", alpha=0.2, label="5-95% Quantile")

plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"{symbol} Price Forecast")
plt.legend()
plt.grid(True)

# Show a little before the forecast starts and all of the forecast
x_min = forecast_df.index[0] - pd.Timedelta(days=n_steps*0.5)
x_max = forecast_df.index[-1]
plt.xlim(left=x_min, right=x_max)

# Save
out_path = Path(f"reports/{symbol}/figures/{symbol}_forecast.png")
out_path.parent.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(out_path)
plt.close()