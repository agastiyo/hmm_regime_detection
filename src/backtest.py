from utils.config import load_config
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

cfg = load_config()
symbol = cfg['data']['symbol']
price = cfg['data']['price_col']

df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_probs_states.csv", parse_dates=['date'], usecols=['date','state',price]).set_index('date')
init_money = df[price].iloc[0]  # Initial investment amount is one share

# Testing 4 strategies: Buy-and-Hold, Risk-Averse, Risk-Seeking, and Dollar-Cost Averaging

# Buy-and-Hold strategy
df['buy_and_hold'] = df[price] * (init_money / df[price].iloc[0]) # Buy-and-Hold strategy

# Risk-Averse and Risk-Seeking strategies
df['risk_averse'] = init_money
df['risk_seeking'] = init_money

for day in range(1, len(df)):
  if df['state'].iloc[day] == 0:  # Low volatility
    df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_averse'] / df.loc[df.index[day-1], price])
    df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day-1], 'risk_seeking']
  else:  # High volatility
    df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day-1], 'risk_averse']
    df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_seeking'] / df.loc[df.index[day-1], price])

# Dollar-Cost Averaging strategy
df['dollar_cost_averaging'] = init_money / len(df)
df['dollar_cost_averaging'] = df['dollar_cost_averaging'].cumsum() * (df[price] / df[price].iloc[0])

p = Path(f"reports/{symbol}/tables/{symbol}_strategies.csv")
p.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(p, index=True)

# Plot Backtest Results in a grid with price and regime for all strategies
fig, axes = plt.subplots(2, 2, figsize=(18, 12), sharex=True)
strategies = ['buy_and_hold', 'risk_averse', 'risk_seeking', 'dollar_cost_averaging']
titles = ['Buy-and-Hold', 'Risk-Averse', 'Risk-Seeking', 'Dollar-Cost Averaging']

for i, ax in enumerate(axes.flatten()):
  # Plot strategy portfolio value
  ax.plot(df.index, df[strategies[i]], label=titles[i], color='black')
  # Plot price on secondary y-axis
  ax.plot(df.index, df[price], label='Price', color='gray', alpha=0.5)
  # Plot regime (state) as scatter
  low_vol = df['state'] == 0
  high_vol = df['state'] == 1
  ax.scatter(df.index[low_vol], df[strategies[i]][low_vol], 
         color='green', marker='o', label='Low Volatility', s=10)
  ax.scatter(df.index[high_vol], df[strategies[i]][high_vol], 
         color='red', marker='o', label='High Volatility', s=10)
  ax.set_title(titles[i])
  ax.set_ylabel("Value ($)")
  # Legends
  lines, labels = ax.get_legend_handles_labels()
  ax.legend(loc='upper left')

axes[-1, 0].set_xlabel("Date")
axes[-1, 1].set_xlabel("Date")
plt.suptitle(f"Backtest Results for {symbol}", fontsize=18)
plt.tight_layout(rect=[0, 0.03, 1, 0.97])

p = Path(f"reports/{symbol}/figures/{symbol}_backtest_results.png")
p.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(p)