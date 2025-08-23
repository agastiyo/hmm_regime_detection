# Hidden Markov Models for Volatility-Aware Strategies

By Agastya Gaur  
August 2025

## Introduction

In this project, I trained a 2-state Gaussian Hidden Markov Model (HMM) on historical asset data to identify windows of low and high volatility.  
The choice of a 2-state model was deliberate: categorizing periods as either calm or turbulent provides an intuitive concept for beginners in trading. Markets often oscillate between “quiet” and “volatile” regimes, making regime-switching models especially useful.  

**Research Question:**  
Do volatility-aware strategies outperform “beginner” strategies over long periods of time?

---

## Data and Preprocessing

A total of 8 assets were chosen for this project:

- **Indexes:** SPY, QQQ, DIA  
- **Stocks:** BRK.A, IBM, META  
- **Commodities and Bonds:** GLD, TLT  

This assures a broad sample of assets to test the strategies.  

**Note:** One limitation of my model was its inability to handle stock splits correctly. Therefore, I restricted the analysis to assets with little or no history of splits.  

Data was collected from AlphaVantage, with coverage dating back to March 20, 2000 (May 18, 2012 for META). The raw data included daily *open, high, low, close* prices, along with volume, and was indexed by date.  

For this project, I focused on **close-to-close daily returns**. Data preprocessing included:

- Removing duplicates and empty rows  
- Converting empty strings to `NaN`  
- Casting all numerical values into float or integer types  

---

## Methodology

### Returns

For each asset, simple and logarithmic returns were calculated (excluding the first day):

- **Simple Return:**
\[
R_t = \frac{P_t - P_{t-1}}{P_{t-1}}
\]

- **Logarithmic Return:**
\[
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
\]

where \( P_t \) is the closing price at time \( t \).  

---

### Hidden Markov Model

The logarithmic returns were fed into a 2-state Gaussian HMM.  
The model outputs:

- Hidden states (low and high volatility)  
- State probabilities  
- Transition matrix  

**Transition matrix:**
\[
T =
\begin{bmatrix}
P(L \to L) & P(L \to H) \\
P(H \to L) & P(H \to H)
\end{bmatrix}
\]

where \( L \) = low volatility, \( H \) = high volatility.  

**Expected regime duration:**
\[
\text{Expected duration in state } i = \frac{1}{1 - P(i \to i)}
\]

---

### Visualizations

- [Insert graphs of returns colored by regime for each asset]  
- [Insert transition matrices for each asset]  
- [Insert table of expected regime durations]  

---

## Backtesting Strategies

With the regimes identified, four trading strategies were backtested.  
Each strategy began with **1000 shares (or equivalent fractional purchases in DCA)** at the start of the period. A transaction cost of 0.1% was applied for each buy/sell action.  

**Baseline Strategies:**

1. **Buy-and-Hold (B&H):** Buy 1000 shares at the beginning and hold until the end.  
2. **Dollar-Cost Averaging (DCA):** Buy equal fractions daily such that 1000 shares are accumulated by the end.  

**Volatility-Aware Strategies:**

1. **Risk-Averse:** Fully invested during low volatility; exit to cash during high volatility.  
2. **Risk-Seeking:** Fully invested during high volatility; exit to cash during low volatility.  

---

## Results

Preliminary results suggest:

- **Risk-Averse** produced the strongest performance.  
- **Buy-and-Hold** followed closely.  
- **Dollar-Cost Averaging** underperformed relative to Buy-and-Hold.  
- **Risk-Seeking** was the weakest strategy.  

---

### Performance Metrics

The following metrics were used to evaluate performance:

- **Final Value (FV):**
\[
FV = \text{Portfolio value at final date}
\]

- **Log Return:**
\[
R_{\text{log}} = \ln\left(\frac{FV}{IV}\right)
\]

- **Compound Annual Growth Rate (CAGR):**
\[
CAGR = \left(\frac{FV}{IV}\right)^{\frac{1}{Y}} - 1
\]
where \( IV \) = initial value, \( Y \) = number of years.  

- **Maximum Drawdown (MDD):**
\[
MDD = \max_{t} \left( \frac{\text{Peak}_t - \text{Trough}_t}{\text{Peak}_t} \right)
\]

- **Calmar Ratio:**
\[
\text{Calmar} = \frac{CAGR}{MDD}
\]

---

### Tables and Graphs

- [Insert table of results: FV, log return, CAGR, MDD, Calmar Ratio by asset and strategy]  
- [Insert portfolio value plots comparing all 4 strategies per asset]  

---

## Forecasting with HMM

To extend the analysis, I explored whether HMM probabilities could be used to predict future regimes and employ volatility-aware strategies prospectively.  

I used the transition matrix and Monte Carlo simulations to forecast regime paths and generate probability distributions for future states.  

**Findings:**

- Point predictions were unreliable due to oversimplification from the 2-state model.  
- Transition matrices tended to be “sticky,” causing the system to fall into long equilibrium states without capturing the actual regime switching observed in real data.  
- Forecasting cannot account for exogenous real-world shocks (e.g., earnings surprises, geopolitical events).  

---

## Discussion

Key limitations:  

- A 2-state model may oversimplify market dynamics.  
- Forecast accuracy was hindered by sticky transition probabilities.  
- The model works retrospectively but struggles prospectively.  

Nevertheless, results suggest that incorporating volatility regimes can improve trading strategies compared to baseline methods.  

---

## Future Work

- Test shorter time horizons (e.g., intraday or minute-level data).  
- Expand to 3- or 4-state Gaussian HMMs to capture finer regimes.  
- Compare with alternative regime-switching models (e.g., Markov-Switching GARCH).  
- Incorporate transaction cost sensitivity analysis.  
- Explore reinforcement learning approaches to adapt strategies dynamically.  

---
