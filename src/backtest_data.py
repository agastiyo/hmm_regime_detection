from utils.config import load_config
import pandas as pd
import numpy as np
from pathlib import Path

cfg = load_config()
symbol = cfg["data"]["symbol"]

strat_df = pd.read_csv(f"reports/{symbol}/tables/{symbol}_strategies.csv", parse_dates=['date']).set_index('date')


d = {'Strategy': ['Buy and Hold', 'Dollar Cost Averaging', 'Risk Averse', 'Risk Seeking']}

metric_df = pd.DataFrame(data=d).set_index('Strategy')

strats = [
  ('buy_and_hold', 'Buy and Hold'),
  ('dollar_cost_averaging', 'Dollar Cost Averaging'),
  ('risk_averse', 'Risk Averse'),
  ('risk_seeking', 'Risk Seeking')
]

for s in strats:
    metric_df.loc[s[1], 'Final Value ($)'] = strat_df[s[0]].iloc[-1].round(2)
    
    metric_df.loc[s[1], 'Total Log Return (%)'] = (((strat_df[s[0]].iloc[-1] / strat_df['close'].iloc[0]) - 1) * 100).round(2)
    
    metric_df.loc[s[1], 'Volatility (%)'] = (np.std(np.log(strat_df[s[0]]/strat_df[s[0]].shift(1)).dropna()) * np.sqrt(252) * 100).round(2)
    
    metric_df.loc[s[1], 'CAGR (%)'] = (((strat_df[s[0]].iloc[-1] / strat_df['close'].iloc[0]) ** (1 / (len(strat_df) / 252)) - 1) * 100).round(2)
    
    rolling_max = strat_df[s[0]].cummax()
    daily_drawdown = strat_df[s[0]] / rolling_max - 1.0
    max_drawdown = daily_drawdown.cummin().min()
    metric_df.loc[s[1], 'Max Drawdown (%)'] = (max_drawdown * 100).round(1)
    
    if max_drawdown != 0:
        metric_df.loc[s[1], 'Calmar Ratio'] = (metric_df.loc[s[1], 'CAGR (%)'] / abs(max_drawdown * 100)).round(3)
        
p = Path(f"reports/{symbol}/tables/{symbol}_metrics.csv")
p.parent.mkdir(parents=True, exist_ok=True)
metric_df.to_csv(p)