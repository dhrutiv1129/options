import yfinance as yf
import numpy as np
from datetime import datetime

def fetch_data(ticker, period="1y"):
    data = yf.download(ticker, period=period, progress=False, auto_adjust=True)
    return data["Close"]

def calculate_annual_volatility(close_prices):
    log_returns = np.log(close_prices / close_prices.shift(1)).dropna()
    return log_returns.std() * np.sqrt(252)

def american_option_price(S0, K, T, r, sigma, option_type="put", steps=100):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    asset_prices = np.zeros(steps + 1)
    option_values = np.zeros(steps + 1)

    for i in range(steps + 1):
        asset_prices[i] = S0 * (u ** (steps - i)) * (d ** i)
        if option_type == "put":
            option_values[i] = max(K - asset_prices[i], 0)
        else:
            option_values[i] = max(asset_prices[i] - K, 0)

    for step in range(steps - 1, -1, -1):
        for i in range(step + 1):
            continuation_value = np.exp(-r * dt) * (p * option_values[i] + (1 - p) * option_values[i + 1])
            asset_price = S0 * (u ** (step - i)) * (d ** i)
            if option_type == "put":
                exercise_value = max(K - asset_price, 0)
            else:
                exercise_value = max(asset_price - K, 0)
            option_values[i] = max(continuation_value, exercise_value)

    return option_values[0]

def should_exercise_early(current_price, strike, option_market_price, option_type):
    if option_type == "put":
        intrinsic_value = max(strike - current_price, 0)
    elif option_type == "call":
        intrinsic_value = max(current_price - strike, 0)
    else:
        raise ValueError("Invalid option type")

    time_value = option_market_price - intrinsic_value
    return time_value < 0.01 and intrinsic_value > 0


     
