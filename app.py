# Interactive dashboard
# run with:  streamlit run app.py

import os

import pandas as pd
import streamlit as st

from utils import SEASON_ORDER

st.set_page_config(page_title="Electricity Dashboard", page_icon="⚡", layout="wide")


@st.cache_data
def get_data():
    # hourly totals made by 01_data_cleaning.py (small enough to keep on GitHub)
    return pd.read_csv("data/hourly_data.csv", index_col="DateTime", parse_dates=True)


def avg_kw(data, by=None):
    # average power = energy used / time, so hours with a few missing minutes don't skew it
    if by is None:
        return data["Energy_kWh"].sum() / data["Minutes"].sum() * 60
    sums = data.groupby(by)[["Energy_kWh", "Minutes"]].sum()
    return sums["Energy_kWh"] / sums["Minutes"] * 60


df = get_data()

st.title("⚡ Household Electricity Consumption Dashboard")
st.caption("UCI Individual Household Electric Power Consumption dataset - one house near Paris, Dec 2006 to Nov 2010")

# ---- sidebar filters ----
st.sidebar.header("Filters")
all_years = sorted(df["Year"].unique())
years = st.sidebar.multiselect("Year", all_years, default=all_years)
seasons = st.sidebar.multiselect("Season", SEASON_ORDER, default=SEASON_ORDER)
day_type = st.sidebar.radio("Day type", ["All", "Weekday", "Weekend"])

filtered = df[df["Year"].isin(years) & df["Season"].isin(seasons)]
if day_type != "All":
    filtered = filtered[filtered["DayType"] == day_type]

if filtered.empty:
    st.warning("No data for the selected filters")
    st.stop()

hourly = avg_kw(filtered, "Hour")

# ---- KPI cards ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average power", f"{avg_kw(filtered):.2f} kW")
col2.metric("Peak hour", f"{hourly.idxmax()}:00")
col3.metric("Max reading", f"{filtered['Max_power'].max():.2f} kW")
col4.metric("Total energy", f"{filtered['Energy_kWh'].sum() / 1000:,.1f} MWh")

# ---- charts ----
st.subheader("Monthly average consumption")
st.line_chart(avg_kw(filtered, pd.Grouper(freq="ME")), y_label="kW")

left, right = st.columns(2)

with left:
    st.subheader("Average by hour of day")
    st.bar_chart(hourly, y_label="kW")

with right:
    st.subheader("Weekday vs weekend")
    st.line_chart(avg_kw(filtered, ["Hour", "DayType"]).unstack(), y_label="kW")

left, right = st.columns(2)

with left:
    st.subheader("Average by season")
    st.bar_chart(avg_kw(filtered, "Season").reindex(SEASON_ORDER).dropna(), y_label="kW")

with right:
    st.subheader("Energy share by sub-meter")
    total_wh = filtered["Energy_kWh"].sum() * 1000
    share = pd.Series({
        "Kitchen": filtered["Sub_metering_1"].sum(),
        "Laundry": filtered["Sub_metering_2"].sum(),
        "Water heater & AC": filtered["Sub_metering_3"].sum(),
    }) / total_wh * 100
    share["Other"] = 100 - share.sum()
    st.bar_chart(share, y_label="% of energy", horizontal=True)

# ---- forecast results (from 04_forecasting.py) ----
st.subheader("2010 daily load forecast")
if os.path.exists("data/forecast_2010.csv"):
    forecast = pd.read_csv("data/forecast_2010.csv", index_col=0, parse_dates=True)
    st.line_chart(forecast, y_label="kW")
else:
    st.info("Run 04_forecasting.py to see forecast results here")
