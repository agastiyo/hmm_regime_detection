#%%
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.config import load_config

cfg = load_config()
#%%
#This notebook is to plot the processed data with returns to make sure that everything is correct
df = pd.read_csv(cfg["data"]["processed_path"], parse_dates=["date"]).set_index("date")

df.plot(y=cfg["data"]["price_col"], figsize=(12, 6), title=cfg["data"]["symbol"]+" Price")
df.plot(y=cfg["model"]["target_col"], figsize=(12, 6), kind="bar", title="Returns")
# %%
