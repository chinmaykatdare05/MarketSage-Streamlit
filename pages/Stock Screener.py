import streamlit as st

st.set_page_config(
    page_title="MarketSage | Stock Screener", page_icon="📈", layout="wide"
)
st.title("Stock Screener")


rsi_period = st.number_input("RSI Period", min_value=1, max_value=200, value=14)
st.info("Feature is yet to be implemented")
