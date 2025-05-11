import streamlit as st
import pandas as pd


@st.cache_data
def get_index_list() -> list:
    """
    Get a list of NIFTY indices.
    Returns:
        list: A list of NIFTY indices.
    """
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
    return index_list


@st.cache_data
def get_equity_list() -> dict:
    """
    Get a dictionary of equity symbols and their corresponding company names.
    Returns:
        dict: A dictionary with symbols as keys and company names as values.
    """
    return pd.read_csv("equityList.csv", index_col=0)


@st.cache_data
def get_nifty50_list() -> dict:
    """
    Get a dictionary of NIFTY 50 symbols and their corresponding company names.
    Returns:
        dict: A dictionary with symbols as keys and company names as values.
    """
    return pd.read_csv("nifty50List.csv", index_col=0)


@st.cache_data
def get_nifty50_industries() -> list:
    """
    Get a list of NIFTY 50 industries.
    Returns:
        list: A list of NIFTY 50 industries.
    """
    return pd.read_csv("nifty50Industries.csv")


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
