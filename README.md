# Vietnam Stock Market Analysis & Algorithmic Trading System 📈

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Backtesting_Complete-success)
![Data](https://img.shields.io/badge/Data-FiinQuantX-orange)

## 📖 Overview

This project aims to develop a comprehensive algorithmic trading system for the stock market in VietNam including (HOSE, HNX, UPCOM). Our system includes intergrating crawling data, cleaning data, exploratory data analysis, feature engineering and Machine Learning and Deep Learning model to find the optimized time to buy/sell stock, manage the risk, apply the bot to backtest in the real market and allow it to send messages to telegram to users to notify the signal.

## 📊 Key Results

Based on backtesting data from 2025, the strategy significantly demonstrate exceptional capital preservation capabilities and ability to make good decisions.

| Metric | Value |
| :--- | :--- |
| **Total Return** | **+29.35%** |
| **Win Rate** | **76.92%** |

| **Max Drawdown** | **-4.06%** |
| **Total Trades** | 52 |

<img width="1242" height="626" alt="backtest2025" src="https://github.com/user-attachments/assets/fdb30d85-afce-4460-9435-40ab5dbca288" />

> *Backtest Data: Jan 04, 2022 - Sep 12, 2025.

## 🛠️ Methodology

The strategy employs a **4-Layer Filtering Strategy** to eliminate noise and select the highest-potential stocks.

> **Note:** The input data was crawled and thoroughly cleaned, and the specific filtering thresholds utilized below were empirically derived through the **Exploratory Data Analysis (EDA)** process.

### 1. Fundamental Filter
Filters out stocks with poor financial health based on fundamental indicators:
* **Criteria:** $EBIT Margin$, $ROA$, $ROE$, $ROIC$.
* **Thresholds:** Utilizes exchange-specific quantile methods (HOSE, HNX, UPCOM) to ensure alignment with the specific liquidity and scale characteristics of each market.

### 2. Technical Filter
Uses Feature Engineering to identify trends and momentum:
* **RSI:** Flexibly adjusts overbought/oversold thresholds (e.g., HNX uses 25-75, UPCOM uses 20-80).
* **MACD:** Eliminates noise using standard deviation (std) and quantile methods.
* **Bollinger Bands:** Uses Bandwidth to assess volatility.

### 3. Risk Classifier (Machine Learning)
Deploys a **LightGBM Classifier** model to forecast future drawdown risks.
* **Objective:** Exclude stocks with high potential for drawdown (worse than the market's 25th percentile).
* **Performance:** Accuracy across all 3 exchanges achieved > 70%.

### 4. Signal Classifier (Deep Learning)
Deploys an **LSTM (Long Short-Term Memory)** model to capture temporal dependencies.
* **Input:** A sequence of 10 sessions comprising technical indicators and price data.
* **Output:** Classification of Buy/Sell/Hold signals.

## 🤖 Real-time Automation & Alerts

To bridge the gap between backtesting and live trading, the system integrates a **Real-time Notification Bot** powered by the **FiinQuant** library and the **Telegram Bot API**.

### Key Features
* **Instant Alerts:** Sends immediate notifications to a private Telegram group whenever a **BUY** or **SELL** signal is triggered.
* **Comprehensive Trade Details:** Each alert provides actionable data for quick execution:
    * **Signal Type:** 📈 BUY / 📉 SELL
    * **Execution Info:** Ticker (Mã), Price (Giá), Volume (Số lượng).
    * **Rationale:** Explains the trigger reason (e.g., *Trailing Stop*, *Entry Signal*).
    * **Portfolio Health:** Updates on Expected Risk, Total Capital, and Remaining Cash.

<img width="927" height="618" alt="Bot" src="https://github.com/user-attachments/assets/bdb05e6a-4a51-4004-baaa-7e2b27cac791" />

## 📉 EDA Highlights


The project conducted extensive EDA on 3 exchanges to thoroughly understand market behavior:
* **HOSE:** Lowest volatility, suitable for stable investment strategies.
* **UPCOM:** Highest volatility and risk, exhibiting strong seasonality.
* **HNX:** Balanced profile between risk and opportunity.

## ⚙️ Installation

1. **Clone repository:**
   git clone [https://github.com/phamducuong05/StockBot.git](https://github.com/phamducuong05/StockBot.git)
   
