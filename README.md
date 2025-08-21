# HMM Regime Detection

This project detects market regimes (calm/low volatility vs. turbulent/high volatility) in a single asset using a Hidden Markov Model (HMM). It provides a full pipeline from raw data to regime classification, visualization, and reporting.

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

Edit `config/base.yaml` to set your data paths, symbol, and model parameters. Example:

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

### 2. Run the Full Pipeline

```bash
python main.py
```

This will:

- Process raw data and compute returns
- Prepare training and full datasets
- Train the HMM and predict regimes
- Generate plots and output tables in `reports/`

---

## How to Add a New Dataset

1. **Place your raw CSV** in `data/raw/` (e.g., `data/raw/NEW_ASSET.csv`).
2. **Update `config/base.yaml`**:
    - `symbol`: Set to your asset's name (e.g., `NEW_ASSET`)
    - `raw_path`: Path to your new CSV
    - `processed_path`: Where to save processed data (e.g., `data/processed/NEW_ASSET_processed.csv`)
    - `price_col`: The column name for price in your CSV
3. **(Optional) Adjust model parameters** as needed.
4. **Run the pipeline**:

    ```bash
    python main.py
    ```

5. **Results** will be saved in `reports/NEW_ASSET/`.

---

## Script Details

- `main.py`: Runs the full pipeline in order (processing, prep, modeling, plotting).
- `config/base.yaml`: Central place for all configuration.
- `src/process_returns.py`: Loads raw data, computes returns, saves processed data.
- `src/prep_model.py`: Splits data into train/test, saves to temp files.
- `src/run_model.py`: Trains HMM, predicts regimes, saves results.
- `src/plot_results.py`: Plots price, returns, and regime states.

---

## Output

After running, you will find:

- **Processed data**: `data/processed/`
- **Temp files**: `data/temp/<SYMBOL>/`
- **Reports**: `reports/<SYMBOL>/tables/` and `reports/<SYMBOL>/figures/`

---

## Notes

- The pipeline expects your CSV to have a `date` column and a price column (e.g., `close`).
- All configuration is handled via `config/base.yaml`.
- For custom analysis, see the `notebooks/` folder.

---
