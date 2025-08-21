import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM

from utils.config import load_config

cfg = load_config()
symbol = cfg["data"]["symbol"]

# Load processed, training, and testing data
df = pd.read_csv(cfg["data"]["processed_path"], parse_dates=["date"]).set_index("date")

df_train = pd.read_csv(f"data/temp/{symbol}/{symbol}_train_data.csv", parse_dates=["date"]).set_index("date")
X_train = df_train.values.reshape(-1, 1)

df_test = pd.read_csv(f"data/temp/{symbol}/{symbol}_full_data.csv", parse_dates=["date"]).set_index("date")
X_test = df_test.values.reshape(-1, 1)

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
state_prob = model.predict_proba(X_test)
predicted_states = model.predict(X_test)


# Combine probabilities and state info into a single DataFrame
probs_states_df = pd.DataFrame({
	"low_vol_prob": state_prob[:,0],
	"high_vol_prob": state_prob[:,1],
	"state": predicted_states
}, index=df_test.index)
transition_matrix = pd.DataFrame(model.transmat_.copy(), index=["low_vol", "high_vol"], columns=["low_vol", "high_vol"])

# Save CSVs and collect metadata
csv_info = []

transition_matrix_path = f"reports/{symbol}/tables/{symbol}_transition_matrix.csv"
probs_states_path = f"reports/{symbol}/tables/{symbol}_probs_states.csv"

# Merge the probabilities with the original DataFrame
probs_states_df = probs_states_df.join(df, how='inner')

# Saving the transition matrix, probabilities, and predicted states
for path, df, desc in [
	(transition_matrix_path, transition_matrix, "Transition matrix of HMM states"),
	(probs_states_path, probs_states_df, "State probabilities and predicted HMM state for each date (0=low_vol, 1=high_vol)")
]:
	p = Path(path)
	p.parent.mkdir(parents=True, exist_ok=True)
	df.to_csv(p, index=True)
	csv_info.append({
		"filename": str(p),
		"description": desc,
		"n_rows": len(df),
		"n_columns": len(df.columns),
		"columns": list(df.columns),
		"created_at": datetime.now().isoformat()
	})

# Save metadata JSON
meta_path = f"reports/tables/{symbol}_metadata.json"
with open(meta_path, "w") as f:
	json.dump({
		"csv_files": csv_info,
		"generated_at": datetime.now().isoformat(),
		"symbol": symbol
	}, f, indent=2)