Option Pricing Model (Monte Carlo Simulation)
Implements an option pricing model using the Monte Carlo simulation method to estimate the theoretical value of options.

What It Does
The model simulates thousands of possible future stock price paths based on mathematical assumptions about volatility and market behavior. By calculating the option’s payoff for each of these paths and averaging them, it estimates the fair (theoretical) price of the option.

Key Features
- Simulates stock price movements using Geometric Brownian Motion (GBM)
- Calculates call or put option prices
- Uses risk-free interest rate, volatility, strike price, and time to expiration as inputs


How It Works
- Generate thousands of random stock price paths over a time horizon (e.g., 1 year).
- Calculate the payoff of the option at the end of each path.
- Average the payoffs, then discount them to present value using the risk-free rate.
- The result is the Monte Carlo estimate of the option’s fair value.
