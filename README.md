# Binance Futures Testnet Trading Bot

A production-quality Python trading bot for placing MARKET and LIMIT orders on the Binance Futures Testnet (USDT-M). This project is designed as an internship assignment to demonstrate modular architecture, rigorous input validation, custom error handling, rotating file logging, and a dual command-line/interactive terminal interface.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Setup](#setup)
6. [Binance Testnet Instructions](#binance-testnet-instructions)
7. [How to Create API Keys](#how-to-create-api-keys)
8. [Usage Instructions](#usage-instructions)
    - [Running Market Orders](#running-market-orders)
    - [Running Limit Orders](#running-limit-orders)
    - [Interactive CLI Mode](#interactive-cli-mode)
9. [Sample Outputs](#sample-outputs)
10. [Assumptions](#assumptions)

---

## Project Overview
This trading bot is built in Python 3.x to interact with the Binance USDT-Margined Futures Testnet platform. It leverages the official `python-binance` client wrapper to safely authenticate, ping the network, and execute buy/sell actions with real-time feedback.

---

## Features
- **Dual Operating Modes**: Supports both automated CLI arguments (`argparse`) and a step-by-step interactive CLI menu.
- **Robust Validation**: Enforces symbols, sides (`BUY`/`SELL`), types (`MARKET`/`LIMIT`), quantities, and prices prior to hitting exchange servers.
- **Professional Log Rotation**: Log file `logs/trading.log` tracks all timestamps, parameters, responses, and API/validation errors. Files auto-rotate at 5MB limit.
- **Graceful Error Handling**: Detects connection dropouts, authentication validation issues, and raw API responses, formatting issues cleanly for terminal users.
- **High Readability Terminal Output**: Color-coded feedback for execution success or fail outcomes via `colorama`.

---

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Marks bot as a python package
│   ├── client.py            # Client wrapper connecting to Binance Testnet
│   ├── orders.py            # Order execution methods (market, limit)
│   ├── validators.py        # Input verification rules and exceptions
│   └── logging_config.py    # Logging rotation configuration setup
├── logs/
│   └── trading.log          # Runtime application logs (created automatically)
├── .env.example             # Template file for API secret details
├── cli.py                   # Main runner console interface
├── requirements.txt         # Library dependencies list
└── README.md                # Documentation and guide instructions
```

---

## Installation

1. **Clone or Copy** this project folder directly into your workspace.
2. Make sure you have **Python 3.8+** installed.
3. Open your terminal in the root directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Setup

1. Copy `.env.example` to a new file named `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open the `.env` file and insert your Binance Futures Testnet API credentials:
   ```env
   BINANCE_API_KEY=your_actual_testnet_api_key
   BINANCE_API_SECRET=your_actual_testnet_api_secret
   ```

---

## Binance Testnet Instructions
The **Binance Futures Testnet (USDT-M)** allows you to practice futures trading with virtual funds without using real money.
- Futures Testnet URL: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
- Standard Spot API keys will **not** work on the Futures Testnet. You must generate dedicated keys from the Futures Testnet website.

---

## How to Create API Keys
1. Navigate to the [Binance Futures Testnet URL](https://testnet.binancefuture.com).
2. Log in using your existing Binance account, or create a mock testnet profile using email/phone credentials.
3. Once logged in, look for the **API Key** section (typically located in the bottom dashboard panel or account settings page).
4. Click **Create API Key** and follow the prompts to complete verification.
5. Copy both the **API Key** and the **Secret Key** immediately. Store them in your local `.env` configuration file. Keep these keys private!

---

## Usage Instructions

### Running Market Orders
To place a MARKET buy order:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

To place a MARKET sell order:
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Running Limit Orders
Limit orders require a valid price parameter:
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
```

### Interactive CLI Mode
If you run the bot without arguments, it will automatically launch the **Interactive Menu**:
```bash
python cli.py
```
This will guide you through entering parameters step-by-step and validate your entries in real-time, providing immediate correction prompts for incorrect inputs.

---

## Sample Outputs

### 1. Market Order Success Output
```text
====================
ORDER SUCCESS
====================

Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001

Order ID: 28318413
Status: FILLED
Executed Quantity: 0.001
Average Price: 67250.40
```

### 2. Limit Order Success Output
```text
====================
ORDER SUCCESS
====================

Symbol: BTCUSDT
Side: BUY
Type: LIMIT
Quantity: 0.001

Order ID: 28318420
Status: NEW
Executed Quantity: 0.0
Average Price: 0.00000
```

### 3. Validation Failure Output
```text
ORDER FAILED
Reason: Invalid side 'BUYING'. Must be 'BUY' or 'SELL'.
```

### 4. API / Credentials Error Output
```text
ORDER FAILED
Reason: Binance API Error: APIError(code=-2015): Invalid API-key, IP, or permissions for action.
```

---

## Assumptions
1. **Time in Force**: For LIMIT orders, the Time in Force is hardcoded to `GTC` (Good 'Til Cancelled), which is standard practice for manual limit orders on Binance Futures.
2. **Margin Asset**: The default traded asset type is USDT-Margined contracts. Symbol sizes and tick rules must comply with Binance’s testnet contract specs (e.g. quantity step size 0.001 for BTCUSDT).
3. **Python Environment**: Assumes a standard Python 3.8+ setup with `pip` package manager installed and command prompt access.
