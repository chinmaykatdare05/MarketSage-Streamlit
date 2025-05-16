import streamlit as st
import yfinance as yf
from utils import get_equity_list, get_nifty50_list, format_value
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Page Configuration
st.set_page_config(
    page_title="MarketSage | Stock Information", page_icon="📈", layout="wide"
)
st.title("Stock Information")


# Cache equity data to avoid redundant calls
@st.cache_data
def fetch_equity_data():
    return get_equity_list()


@st.cache_data
def fetch_nifty50_data():
    return get_nifty50_list()


# Cache stock data to avoid redundant API calls
def fetch_stock_data(stock_symbol):
    return yf.Ticker(f"{stock_symbol}.NS")


# Cache NLTK download to avoid repeated downloads
@st.cache_resource
def download_nltk_resources():
    nltk.download("vader_lexicon", quiet=True)
    return SentimentIntensityAnalyzer()


# Stock Selecticon
is_nifty_50 = st.toggle("Include only Nifty 50 Stocks", value=False)
stock = st.selectbox(
    "Stock Selection",
    fetch_nifty50_data().index if is_nifty_50 else fetch_equity_data().index,
    index=None,
    placeholder="Select a stock",
)

# Submit Button
if st.button("Submit"):
    # Fetch Stock Data
    data = fetch_stock_data(stock)
    info = data.info

    # Company Info Section
    st.header(info.get("longName", "N/A"))

    # st.header("Company Information")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Sector", value=info.get("sector", "N/A"))

    with col2:
        st.metric(label="Industry", value=info.get("industry", "N/A"))

    # Technicals Section
    st.divider()
    st.header("Performance")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="52 Week Low", value=f"₹{round(info.get('fiftyTwoWeekLow', 0), 2)}"
        )
        st.metric(
            label="50 Day Moving Average",
            value=f"₹{round(info.get('fiftyDayAverage', 0), 2)}",
        )
        st.metric(label="Beta", value=info.get("beta", "N/A"))

    with col2:
        st.metric(
            label="52 Week High", value=f"₹{round(info.get('fiftyTwoWeekHigh', 0), 2)}"
        )
        st.metric(
            label="200 Day Moving Average",
            value=f"₹{round(info.get('twoHundredDayAverage', 0), 2)}",
        )

    # Financials Section
    st.divider()
    st.header("Fundamentals")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Market Cap", value=f"₹{format_value(info.get('marketCap', 0))}"
        )
        st.metric(
            label="PE Ratio",
            value=f"{round(info.get('trailingPE', 0), 2) if info.get('trailingPE') is not None else 'N/A'}",
        )
        st.metric(
            label="PB Ratio",
            value=f"{round(info.get('priceToBook', 0), 2) if info.get('priceToBook') is not None else 'N/A'}",
        )
        st.metric(
            label="Industry PE",
            value=f"{round(info.get('industryPE', 0), 2) if info.get('industryPE') is not None else 'N/A'}",
        )
        st.metric(
            label="Debt to Equity",
            value=f"{round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') is not None else 'N/A'}",
        )

    with col2:
        st.metric(
            label="Return on Equity (ROE)",
            value=f"{round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') is not None else 'N/A'}%",
        )
        st.metric(
            label="Earnings Per Share (EPS)",
            value=f"₹{round(info.get('trailingEps', 0), 2)}",
        )
        st.metric(
            label="Dividend Yield",
            value=f"{round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') is not None else 'N/A'}%",
        )
        st.metric(
            label="Book Value",
            value=f"₹{round(info.get('bookValue', 0), 2) if info.get('bookValue') is not None else 'N/A'}",
        )
        st.metric(
            label="Face Value",
            value=f"₹{round(info.get('faceValue', 0), 2) if info.get('faceValue') is not None else 'N/A'}",
        )

    with col3:
        st.download_button(
            label="Download Balance Sheet",
            data=data.balance_sheet.to_csv(),
            file_name=f"{stock}_balance_sheet.csv",
            mime="text/csv",
        )
        st.download_button(
            label="Download Dividends",
            data=data.dividends.to_csv(),
            file_name=f"{stock}_dividends.csv",
            mime="text/csv",
        )
        st.download_button(
            label="Download Cash Flow",
            data=data.cash_flow.to_csv(),
            file_name=f"{stock}_cash_flow.csv",
            mime="text/csv",
        )
        st.download_button(
            label="Download Income Statement",
            data=data.income_stmt.to_csv(),
            file_name=f"{stock}_income_stmt.csv",
            mime="text/csv",
        )
        st.download_button(
            label="Download Financials",
            data=data.financials.to_csv(),
            file_name=f"{stock}_financials.csv",
            mime="text/csv",
        )

    st.divider()
    st.header("Financials")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Revenue", value=f"₹{format_value(info.get('totalRevenue', 0))}"
        )
    with col2:
        st.metric(
            label="Gross Profit", value=f"₹{format_value(info.get('grossProfits', 0))}"
        )

    # News and Sentiment Analysis
    sia = download_nltk_resources()

    st.divider()
    st.header("News Sentiment Analysis")
    if data.news:
        sentiments = [
            sia.polarity_scores(article["content"]["summary"])["compound"]
            for article in data.news
        ]

        sentiment_score = (
            round(((sum(sentiments) / len(sentiments)) + 1) * 50) if sentiments else 50
        )
        st.metric(
            label="News Sentiment Score",
            value=f"{sentiment_score}",
            delta=f"{sentiment_score - 50}",
            delta_color="off" if sentiment_score == 50 else "normal",
        )
    else:
        st.markdown("No news available for this stock.")
