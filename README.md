
# HMM Regime Detection

This project aims to:

- **Classify past asset price data as either volatile or non-volatile** (high or low volatility regimes) using a Hidden Markov Model (HMM).
- **Extrapolate the model into the future using Monte Carlo simulation methods** to predict the likely price path and uncertainty at later periods of time.

The pipeline detects market regimes in a single asset, visualizes regime switches, and produces probabilistic price forecasts based on the learned model.

## Features

- **Automated pipeline**: From raw CSV to processed data, model training, and result plots.
- **Configurable**: Easily adjust data paths, model parameters, and target columns via YAML.
- **Extensible**: Add new datasets or change model settings with minimal code changes.

---

## Getting Started

### 1. Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Project Structure

```txt
├── main.py                # Main pipeline script
├── config/base.yaml       # Main configuration file
├── data/                  # Raw and processed data
├── src/                   # Source code (processing, modeling, plotting)
├── reports/               # Output tables and figures
```

---

## Usage

### 1. Configure the Pipeline

Edit `config/base.yaml` to set:

- The asset symbol (e.g., `QQQ`)
- Paths to your raw and processed data
- The price column name (e.g., `close`)
- Model parameters (target column, train/test split, number of iterations, random seed)

Example config:

```yaml
data:
  symbol: QQQ
  raw_path: data/raw/QQQ_full.csv
  processed_path: data/processed/QQQ_full_processed.csv
  price_col: close

model:
  target_col: log_ret
  train_frac: 0.6
  n_iter: 100
  seed: 42
```

### 2. Run the Pipeline

From the project root, run:

```bash
python main.py
```

This will:

- Process raw data and compute returns
- Prepare training and full datasets
- Train the HMM and classify each date as high or low volatility
- Forecast future prices using Monte Carlo simulation
- Generate plots and output tables in `reports/`

---

## Adding a New Dataset

1. Place your raw CSV in `data/raw/` (e.g., `data/raw/NEW_ASSET.csv`).

   - The CSV must have a `date` column and a price column (e.g., `close`).

2. Edit `config/base.yaml`:

   - Set `symbol` to your asset's name (e.g., `NEW_ASSET`)
   - Set `raw_path` and `processed_path` accordingly
   - Set `price_col` to match your CSV

3. (Optional) Adjust model parameters as needed
4. Run the pipeline:

  ```bash
  python main.py
  ```

1. Results will be saved in `reports/NEW_ASSET/`

---

## Script Details

- `main.py`: Runs the full pipeline (processing, prep, modeling, forecasting, plotting)
- `config/base.yaml`: Central configuration file
- `src/process_returns.py`: Loads raw data, computes returns, saves processed data
- `src/prep_model.py`: Splits data into train/test, saves to temp files
- `src/run_model.py`: Trains HMM, predicts regimes, saves results
- `src/forecast.py`: Runs Monte Carlo price forecasting
- `src/plot_results.py` and `src/plot_forecast.py`: Plot price, returns, regimes, and forecasts

---

## Output

After running, you will find:

- Processed data: `data/processed/`
- Temp files: `data/temp/<SYMBOL>/`
- Reports: `reports/<SYMBOL>/tables/` (CSVs) and `reports/<SYMBOL>/figures/` (plots)

---

## Notes

- The pipeline expects your CSV to have a `date` column and a price column (e.g., `close`).
- All configuration is handled via `config/base.yaml`.
- For custom analysis or exploration, see the `notebooks/` folder.
