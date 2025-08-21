import pandas as pd
import matplotlib.pyplot as plt
from utils.config import load_config

cfg = load_config()

price = cfg["data"]["price_col"]
returns = cfg["model"]["target_col"]
symbol = cfg["data"]["symbol"]

df = pd.read_csv(f"reports/tables/{symbol}_probs_states.csv", parse_dates=["date"]).set_index("date")

# Create a single figure with two subplots sharing the x-axis
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

# Price with Regime Coloring
ax1.plot(df.index, df[price], label=price, color='black', linewidth=1.5)
ax1.set_ylabel(price)

# Overlay volume on a secondary y-axis, but scale it down for better visualization
volume = df["volume"]
ax1b = ax1.twinx()
ax1b.plot(df.index, volume, label="Volume (scaled)", color='lightgreen', alpha=0.5)
ax1b.fill_between(df.index, volume, color='lightgreen', alpha=0.2)
ax1b.set_ylabel("Volume")
ax1b.tick_params(axis='y')

# Regime coloring
low_vol = df["state"] == 0
high_vol = df["state"] == 1
ax1.scatter(df.index[low_vol], df[price][low_vol], color="green", label="Low Volatility", s=10)
ax1.scatter(df.index[high_vol], df[price][high_vol], color="red", label="High Volatility", s=10)

# Add space below the lowest price and above the volume
min_price = df[price].min()
max_price = df[price].max()
price_padding = (max_price - min_price) * 0.2  # 20% padding
ax1.set_ylim(bottom=min_price - price_padding)

mid_volume = (df["volume"].max() + df["volume"].min())/2
volume_padding = mid_volume * 9  # 900% padding
ax1b.set_ylim(top=mid_volume + volume_padding)

ax1.set_title(f"{cfg['data']['symbol']} Price with Regime Coloring")
ax1.legend(loc="upper left")
ax1.grid(True)

# Returns with Regime Coloring
colors = df["state"].map({0: "green", 1: "red"})
ax2.bar(df.index, df[returns], color=colors, width=1.0)
ax2.set_title(f"{cfg['data']['symbol']} Returns with Regime Coloring")
ax2.set_xlabel("Date")
ax2.set_ylabel(returns)
ax2.grid(True)

plt.tight_layout()
plt.savefig(f"reports/figures/{cfg['data']['symbol']}_price_and_return_with_regime.png")
plt.close()
