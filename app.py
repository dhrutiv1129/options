import streamlit as st
from datetime import datetime
from finance import fetch_data, calculate_annual_volatility, american_option_price, should_exercise_early

st.set_page_config(page_title="American Option Pricer", page_icon="📈")

st.title("📈 American Option Pricer")

with st.form("option_pricer_form"):
    ticker = st.text_input("Enter the stock ticker (e.g., AAPL):", "MSFT").upper()
    option_type = st.selectbox("Option type:", ["put", "call"])
    strike = st.number_input("Enter the strike price:", min_value=1.0, value=300.0, step=1.0)
    expiration = st.date_input("Enter expiration date:", datetime(2026, 6, 24))

    submitted = st.form_submit_button("Calculate Option Price")

if submitted:
    st.subheader("🔎 Pricing Results")
    try:
        close_prices = fetch_data(ticker)
        S0 = close_prices.iloc[-1].item()
        sigma = calculate_annual_volatility(close_prices).item()
        T = (expiration - datetime.today().date()).days / 365
        r = 0.05

        option_price = american_option_price(S0, strike, T, r, sigma, option_type)
        exercise_advice = should_exercise_early(S0, strike, option_price, option_type)

        st.write(f"**Ticker:** {ticker}")
        st.write(f"**Current Price (S₀):** ${S0:.2f}")
        st.write(f"**Volatility (σ):** {sigma:.4f}")
        st.write(f"**Option Price ({option_type}):** ${option_price:.2f}")
        st.write(f"**Strike Price (K):** ${strike}")
        st.write(f"**Expires:** {expiration}")
        st.markdown("### 📌 Early Exercise Recommendation")
        if exercise_advice:
            st.success("🟢 You may consider early exercising this option.")
        else:
            st.warning("🔴 Do NOT early exercise this option.")

    except Exception as e:
        st.error(f"Error: {e}")
