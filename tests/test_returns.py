from pathlib import Path

import numpy as np
import pandas as pd
import pandas.api.types as pdt
from src.utils.config import load_config

# To run in terminal:
# python3 -m pytest -q

cfg = load_config()
DATA_PATH = Path(cfg["data"]["processed_path"])

def load_df():
  assert DATA_PATH.exists(), f"Missing processed CSV at {DATA_PATH}. Run src/returns.py first."
  df = pd.read_csv(DATA_PATH, parse_dates=["date"]).sort_values("date").set_index("date")
  return df


def test_index_is_datetime_and_sorted():
    df = load_df()
    # index type
    assert df.index.inferred_type in ("datetime64", "datetime64tz")
    # strictly increasing
    assert df.index.is_monotonic_increasing
    # no duplicates
    assert not df.index.duplicated().any()


def test_expected_columns_present():
    df = load_df()
    required = {"open", "high", "low", "close", "adj_close", "volume", "simple_ret", "log_ret"}
    missing = required.difference(df.columns)
    assert not missing, f"Missing required columns: {missing}"


def test_numeric_dtypes():
    df = load_df()
    numeric_cols = ["open", "high", "low", "close", "adj_close", "volume", "simple_ret", "log_ret"]
    for c in numeric_cols:
        assert c in df.columns, f"Column {c} missing"
        assert pdt.is_numeric_dtype(df[c]), f"Column {c} is not numeric dtype, got {df[c].dtype}"


def test_returns_math():
    df = load_df()
    # First return should be NaN due to shift(1)
    assert pd.isna(df["simple_ret"].iloc[0]), "First simple_ret should be NaN"
    assert pd.isna(df["log_ret"].iloc[0]), "First log_ret should be NaN"
    # Relationship between log and simple returns: exp(log) - 1 == simple
    left = np.expm1(df["log_ret"].dropna().values)
    right = df["simple_ret"].dropna().values
    np.testing.assert_allclose(left, right, rtol=1e-10, atol=1e-12)


def test_no_inf_and_reasonable_magnitudes():
    df = load_df()
    sr = df["simple_ret"].dropna()
    lr = df["log_ret"].dropna()
    # No infs
    assert np.isfinite(sr).all(), "simple_ret contains non-finite values"
    assert np.isfinite(lr).all(), "log_ret contains non-finite values"
    # For this synthetic daily series, returns should be modest
    assert sr.abs().max() < 0.2, f"Unreasonably large daily return detected: {sr.abs().max():.4f}"


def test_close_to_close_definition():
    df = load_df()
    # Recompute simple returns from adj_close to verify no lookahead and correct base
    px = df["adj_close"].astype(float)
    prev = px.shift(1)
    simple_check = (px / prev) - 1.0
    # Compare where both are defined
    mask = simple_check.notna() & df["simple_ret"].notna()
    np.testing.assert_allclose(simple_check[mask].values, df["simple_ret"][mask].values, rtol=1e-12, atol=1e-12)