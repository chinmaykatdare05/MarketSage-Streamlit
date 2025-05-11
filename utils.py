import streamlit as st
from typing import Dict, List
from nselib import capital_market
import pandas as pd

# For Deployment
import requests
from io import StringIO


@st.cache_data
def get_equity_data() -> Dict[str, str]:
    """
    Fetch equity list and create a dictionary mapping symbol to company name
    """
    # For Delpoyment
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    csv_text = response.text

    equity_list = pd.read_csv(StringIO(csv_text))
    symbols: pd.Series = equity_list.get("SYMBOL", pd.Series())
    names: pd.Series = equity_list.get("NAME OF COMPANY", pd.Series())
    return {"Symbol": symbols.tolist(), "Company Name": names.tolist()}

    # For Local Usage and Testing
    # equity_list: pd.DataFrame = capital_market.equity_list()
    # symbols: pd.Series = equity_list.get("SYMBOL", pd.Series())
    # names: pd.Series = equity_list.get("NAME OF COMPANY", pd.Series())
    # return {"Symbol": symbols.tolist(), "Company Name": names.tolist()}


@st.cache_data
def get_nifty50_data() -> Dict[str, str]:
    """
    Fetch Nifty 50 list and create a dictionary mapping symbol to company name
    """
    nifty50_list: pd.DataFrame = capital_market.nifty50_equity_list()
    symbols: pd.Series = nifty50_list.get("Symbol", pd.Series())
    names: pd.Series = nifty50_list.get("Company Name", pd.Series())
    return {"Symbol": symbols.tolist(), "Company Name": names.tolist()}


@st.cache_data
def get_nifty50_industries() -> List[str]:
    """
    Fetch unique industries from Nifty 50 list
    """
    nifty50_list: pd.DataFrame = capital_market.nifty50_equity_list()
    industries: pd.Series = nifty50_list.get("Industry", pd.Series())
    return {"Industries": industries.dropna().unique().tolist()}


index_list = [
    "NIFTY 50",
    "NIFTY NEXT 50",
    "NIFTY MIDCAP 50",
    "NIFTY MIDCAP 100",
    "NIFTY MIDCAP 150",
    "NIFTY SMALLCAP 50",
    "NIFTY SMALLCAP 100",
    "NIFTY SMALLCAP 250",
    "NIFTY MIDSMALLCAP 400",
    "NIFTY 100",
    "NIFTY 200",
    "NIFTY AUTO",
    "NIFTY BANK",
    "NIFTY ENERGY",
    "NIFTY FINANCIAL SERVICES",
    "NIFTY FINANCIAL SERVICES 25/50",
    "NIFTY FMCG",
    "NIFTY IT",
    "NIFTY MEDIA",
    "NIFTY METAL",
    "NIFTY PHARMA",
    "NIFTY PSU BANK",
    "NIFTY REALTY",
    "NIFTY PRIVATE BANK",
    "Securities in F&O",
    "Permitted to Trade",
    "NIFTY DIVIDEND OPPORTUNITIES 50",
    "NIFTY50 VALUE 20",
    "NIFTY100 QUALITY 30",
    "NIFTY50 EQUAL WEIGHT",
    "NIFTY100 EQUAL WEIGHT",
    "NIFTY100 LOW VOLATILITY 30",
    "NIFTY ALPHA 50",
    "NIFTY200 QUALITY 30",
    "NIFTY ALPHA LOW-VOLATILITY 30",
    "NIFTY200 MOMENTUM 30",
    "NIFTY COMMODITIES",
    "NIFTY INDIA CONSUMPTION",
    "NIFTY CPSE",
    "NIFTY INFRASTRUCTURE",
    "NIFTY MNC",
    "NIFTY GROWTH SECTORS 15",
    "NIFTY PSE",
    "NIFTY SERVICES SECTOR",
    "NIFTY100 LIQUID 15",
    "NIFTY MIDCAP LIQUID 15",
]


def format_value(number: float) -> str:
    """
    Format a large number into a simplified text representation.
    Examples:
        70000000 -> '7Cr'
        1000000000 -> '1000Cr'
        230000 -> '2.3L'
    """
    if number >= 10**7:
        return (
            f"{number / 10**7:.1f}Cr" if number % 10**7 != 0 else f"{number // 10**7}Cr"
        )
    elif number >= 10**5:
        return (
            f"{number / 10**5:.1f}L" if number % 10**5 != 0 else f"{number // 10**5}L"
        )
    else:
        return str(number)
