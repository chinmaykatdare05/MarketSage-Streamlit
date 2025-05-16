import streamlit as st
import pandas as pd
import yfinance as yf
from utils import get_equity_list
import plotly.figure_factory as ff

# Set the page configuration
st.set_page_config(
    page_title="MarketSage | Home",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

st.logo("./logo.png", size="large", icon_image="./logo.png")

# Download stock data and plot the close price
st.title("MarketSage Home Page")

option = st.selectbox(
    "Select a Stock",
    get_equity_list().index,
    index=None,
    placeholder="Select a stock",
)


# Download stock data
@st.cache_data
def download_stock_data(ticker: str) -> pd.DataFrame:
    """
    Download stock data from Yahoo Finance.
    """
    return yf.download(ticker)


if option:
    try:
        df = download_stock_data(f"{option}.NS")
        if not df.empty:
            mode = st.pills(
                "Plot type",
                options=["Candlestick", "Line", "Area"],
                default="Candlestick",
                selection_mode="single",
            )
            if mode == "Line":
                st.line_chart(df["Close"], use_container_width=True)
            elif mode == "Area":
                st.area_chart(df["Volume"], use_container_width=True)
            else:
                fig = ff.create_candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="Candlestick Chart",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"No data available for the selected stock: {option}")
    except Exception as e:
        st.error(f"An error occurred while processing data for {option}: {e}")
        # Display the data
        st.subheader(f"Data for {option}")
        st.dataframe(df, use_container_width=True)
else:
    st.info("Please select a stock to view data.")
