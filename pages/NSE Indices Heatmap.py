import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from utils import get_index_list

# Page config
st.set_page_config(
    page_title="MarketSage | NSE Indices Heatmap", page_icon="📈", layout="wide"
)
st.title("NSE Indices Heatmap")


# Cache API responses for 5 minutes
@st.cache_data(ttl=300)
def get_index_details(category):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    category = category.upper().replace("&", "%26").replace(" ", "%20")
    try:
        ref = requests.get(
            f"https://www.nseindia.com/market-data/live-equity-market?symbol={category}",
            headers=headers,
        )
        url = f"https://www.nseindia.com/api/equity-stockIndices?index={category}"
        data = requests.get(url, headers=headers, cookies=ref.cookies.get_dict()).json()
        df = pd.DataFrame(data["data"])
        if not df.empty:
            df = df.drop(["meta"], axis=1)
            df = df.set_index("symbol", drop=True)
            df["ffmc"] = round(df["ffmc"] / 1e7, 0)
            df = df.iloc[1:].reset_index()
        return df

    except Exception as e:
        st.error("Error fetching data from NSE.")
        return pd.DataFrame()


# Index options


# Title and index selection
col1, col2, col3 = st.columns([1, 1, 1])
index_filter = col1.selectbox("Select Index", get_index_list())
slice_by = col2.selectbox("Slice By", ["Market Cap", "Gainers", "Losers"])

# Fetch data
df = get_index_details(index_filter)

# Pie Chart Summary
if not df.empty:
    adv, dec, no_chg = (
        df[df["pChange"] > 0].shape[0],
        df[df["pChange"] < 0].shape[0],
        df[df["pChange"] == 0].shape[0],
    )

    pie_fig = px.pie(
        names=["Advances", "Declines", "No Change"],
        values=[adv, dec, no_chg],
        color=["Advances", "Declines", "No Change"],
        color_discrete_sequence=["#046A38", "#FF671F", "#FFFFFF"],
        hole=0.6,
    )
    pie_fig.update_traces(textinfo="none")
    pie_fig.update_layout(
        width=250,
        height=250,
        showlegend=False,
        annotations=[
            dict(
                text=f"{adv} ↑<br>{dec} ↓",
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False,
            )
        ],
        margin=dict(l=0, r=0, t=0, b=0),
    )

    if slice_by == "Market Cap":
        metric = "ffmc"
        colors = ["#FF671F", "#FFFFFF", "#046A38"]
    elif slice_by == "Gainers":
        metric = "pChange"
        colors = ["#FFFFFF", "#046A38"]
    else:  # Losers
        df = df[df["pChange"] < 0]
        df["Abs"] = df["pChange"].abs()
        metric = "Abs"
        colors = ["#FF671F", "#FFFFFF"]

    treemap = px.treemap(
        df,
        path=["symbol"],
        values=metric,
        color="pChange",
        color_continuous_scale=colors,
        custom_data=["pChange"],
    )
    treemap.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )
    treemap.update_traces(
        hovertemplate="<b>%{label}</b><br>Size: %{value}<br>pChange: %{customdata[0]:.2f}%",
        texttemplate="%{label}<br>%{customdata[0]:.2f}%",
        textposition="middle center",
    )
    treemap.update_coloraxes(showscale=False)
    st.plotly_chart(treemap, use_container_width=True)

    col3.plotly_chart(pie_fig)

else:
    st.warning("No data returned. Please try another index or try again later.")
