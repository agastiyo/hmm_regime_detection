import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from utils.config import load_config

cfg = load_config()
symbol = cfg["data"]["symbol"]

# Load training and testing data
df_train = pd.read_csv(f"data/temp/{symbol}_train_data.csv", parse_dates=["date"]).set_index("date")
X_train = df_train.values.reshape(-1, 1)

df_full = pd.read_csv(f"data/temp/{symbol}_full_data.csv", parse_dates=["date"]).set_index("date")
X_full = df_full.values.reshape(-1, 1)

# Running the 2 state Gaussian HMM
model = GaussianHMM(n_components=2, covariance_type='diag', n_iter=cfg["model"]["n_iter"], random_state=cfg["model"]["seed"])
model.fit(X_train)

variances = model.covars_.ravel()
order = np.argsort(variances)

model.means_ = model.means_[order]
model.covars_ = model.covars_[order].reshape(2,1)
model.startprob_ = model.startprob_[order]
model.transmat_ = model.transmat_[np.ix_(order, order)]

# Predicting the hidden states for the test data
hidden_states = model.predict_proba(X_full)
valid_index = df_full.index

# Creating a DataFrame to hold the probabilities of each state
probs = pd.DataFrame({"low_vol": hidden_states[:,0], "high_vol": hidden_states[:,1]}, index=valid_index)
transition_matrix = pd.DataFrame(model.transmat_.copy(), index=["low_vol", "high_vol"], columns=["low_vol", "high_vol"])

# Saving the transition matrix and probabilities
p = Path(f"reports/tables/{symbol}_transition_matrix.csv")
p.parent.mkdir(parents=True, exist_ok=True)
transition_matrix.to_csv(p, index=True)

p = Path(f"reports/tables/{symbol}_probabilities.csv")
p.parent.mkdir(parents=True, exist_ok=True)
probs.to_csv(p, index=False)