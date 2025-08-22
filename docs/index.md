# Hidden Markov Models for Volatility-Aware Strategies

## Introduction

In this project, I trained a 2-state Gaussian Hidden Markov Model (HMM) on historical asset data to identify windows of low and high volatility. The choice of a 2-state model was deliberate: categorizing periods as either calm or turbulent provides is an intuitive concept for beginners in trading, and the market tends to cycle often between "quiet" and "volatile", making regime-switching models extremely useful. Investing with strategies based around volatility might prove to be extremely valuable in taking one's trading strategy a step above the tried and tested methods.

Research Question: Do Volatility-Aware Strategies outperform "beginner" strategies over long periods of time?

## Data and Preproscessing

A total of 8 assets were chosen for this project:

Indexes: SPY, QQQ, DIA
Stocks: BRK.A, IBM, META
Commodities and Bonds: GLD, TLT

This assures a broad sample of assets to test the strategies.

Note: One limitation of my model was it's inabilty to handle stock splits correctly, hence the usage of assets with little or no splits.

Asset prices dating back to March 20, 2000 (May 18, 2012 for META) were collected using AlphaVantage. The raw data included daily open, close, high and low prices along with the daily volume and was indexed by date. For this project, I used close-to-close price data.

The data was cleaned up by removing duplicate rows, empty rows, and forcing empty strings to NaN, and all numerical values into integer or float types.

## Methodology

After cleaning up the data, simple and logarthmic returns were calculated for each day (excluding the first).

[Insert equations for these here]

The logarithmic returns were then fed into the 2-state Gaussian HMM, which identifed the low and high volatility states in the data and created a transition matrix for the system.

![alt text](../reports/DIA/figures/DIA_price_and_return_with_regime.png)

[Insert price return with regime graphs for each asset, include their transition matrices as well]

[Include the equation that calculates the predicted amount of time a regieme will last]

[Make a table for the predicted regime durations]

## Backtesting Strategies

With the historical data analyzed and the regiemes predicted, 4 trading strategies were tested.

Each strategy bought one share of the asset at the beginning of the timescale. This tracks the value of the portfolio in the same order of magnitude as the asset price itself. Buying into and selling out of the market at any point incurred a 0.1% transaction cost.

Beginner Strategies (baseline):

1. Buy-and-Hold - buying the stock at the beginning of the timescale and holding indefinitely
2. Dollar-Cost Average - Buying a fraction of the stock every day until complete on the last day in the timescale
  
Volatility-Aware Strategies

1. Risk Averse - All in when the market is calm and all out when volatile
2. Risk Seeking - All out when the market is cal and all in when volatile

## Results

## Forecasting with HMM

## Discussion

## Future Work

## Conclusion
