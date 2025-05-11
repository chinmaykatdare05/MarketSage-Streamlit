import streamlit as st
from utils import get_equity_list, get_nifty50_list, get_nifty50_industries

# Set the page configuration
st.set_page_config(
    page_title="MaarketSage | List of Stocks",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

st.logo("./logo.png", size="large", icon_image="./logo.png")


st.header("List of Stocks")
st.write("Please select a List to View")
list_type = st.selectbox(
    "Select List",
    ("Equity List", "Nifty 50 List", "Nifty 50 Industries"),
)
if list_type == "Equity List":
    st.dataframe(get_equity_list())
elif list_type == "Nifty 50 List":
    st.dataframe(get_nifty50_list())
elif list_type == "Nifty 50 Industries":
    st.dataframe(get_nifty50_industries())
