from utils.config import load_config
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

cfg = load_config()
symbol = cfg['data']['symbol']
price = cfg['data']['price_col']
transaction_cost = 0.001  # Transaction cost per trade (0.1%)

df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_probs_states.csv", parse_dates=['date'], usecols=['date','state',price]).set_index('date')
init_money = df[price].iloc[0] * (1-transaction_cost)  # Initial investment amount is 1 share of the asset minus transaction cost

# Testing 4 strategies: Buy-and-Hold, Risk-Averse, Risk-Seeking, and Dollar-Cost Averaging

# Buy-and-Hold strategy
df['buy_and_hold'] = df[price] * (init_money / df[price].iloc[0])  # Buy-and-Hold strategy

# Risk-Averse and Risk-Seeking strategies
df['risk_averse'] = init_money
df['risk_seeking'] = init_money

for day in range(1, len(df)):
  if df['state'].iloc[day-1] == 0:  # If previous day was low volatility
    if df['state'].iloc[day] == 0:  # If current day is also low volatility
      df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_averse'] / df.loc[df.index[day-1], price]) # Risk averse stays in
      df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day-1], 'risk_seeking'] # Risk seeking stays out
    else: # Current day is high volatility
      df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_averse'] / df.loc[df.index[day-1], price]) * (1 - transaction_cost)  # Risk averse sells out at price minus transaction cost
      df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day-1], 'risk_seeking'] * (1-transaction_cost) # Risk seeking buys in at price minus transaction cost
      
  else:  # If perevious day was high volatility
    if df['state'].iloc[day] == 0:  # If current day is low volatility
      df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day-1], 'risk_averse'] * (1-transaction_cost)  # Risk averse buys in at price minus transaction cost
      df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_seeking'] / df.loc[df.index[day-1], price]) * (1 - transaction_cost)  # Risk seeking sells out at price minus transaction cost
    else:  # Current day is also high volatility
      df.loc[df.index[day], 'risk_averse'] = df.loc[df.index[day-1], 'risk_averse']  # Risk averse stays out
      df.loc[df.index[day], 'risk_seeking'] = df.loc[df.index[day], price] * (df.loc[df.index[day-1], 'risk_seeking'] / df.loc[df.index[day-1], price])  # Risk seeking stays in

# Dollar-Cost Averaging strategy
invest_per_day = (init_money) / len(df)
shares = 0
df['dollar_cost_averaging'] = invest_per_day
for day in range(1,len(df)):
  shares += (invest_per_day * (1-transaction_cost)) / df[price].iloc[day]
  df.loc[df.index[day], 'dollar_cost_averaging'] = shares * df[price].iloc[day]

  
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
  ax.plot(df.index, df[price], label='Closing Price', color='gray', alpha=0.5)
  # Plot regime (state) as scatter
  low_vol = df['state'] == 0
  high_vol = df['state'] == 1
  ax.scatter(df.index[low_vol], df[strategies[i]][low_vol], 
         color='green', marker='o', label='Low Volatility', s=10)
  ax.scatter(df.index[high_vol], df[strategies[i]][high_vol], 
         color='red', marker='o', label='High Volatility', s=10)
  ax.set_title(titles[i])
  ax.set_ylabel("Price / Portfolio Value")
  # Legends
  
  ax.legend(loc='upper left')

axes[-1, 0].set_xlabel("Date")
axes[-1, 1].set_xlabel("Date")
plt.suptitle(f"Backtest Results for {symbol}", fontsize=18)
plt.tight_layout(rect=[0, 0.03, 1, 0.97])

p = Path(f"reports/{symbol}/figures/{symbol}_backtest_results.png")
p.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(p)