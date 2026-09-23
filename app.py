# Interactive dashboard
# run with:  streamlit run app.py

import os

import pandas as pd
import streamlit as st

from utils import load_clean_data, SEASON_ORDER

st.set_page_config(page_title="Electricity Dashboard", page_icon="⚡", layout="wide")


@st.cache_data
def get_data():
    return load_clean_data()


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

power = filtered["Global_active_power"]
hourly = power.groupby(filtered["Hour"]).mean()

# ---- KPI cards ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average power", f"{power.mean():.2f} kW")
col2.metric("Peak hour", f"{hourly.idxmax()}:00")
col3.metric("Max reading", f"{power.max():.2f} kW")
col4.metric("Total energy", f"{power.sum() / 60 / 1000:,.1f} MWh")

# ---- charts ----
st.subheader("Monthly average consumption")
st.line_chart(power.resample("ME").mean(), y_label="kW")

left, right = st.columns(2)

with left:
    st.subheader("Average by hour of day")
    st.bar_chart(hourly, y_label="kW")

with right:
    st.subheader("Weekday vs weekend")
    by_daytype = filtered.pivot_table(index="Hour", columns="DayType",
                                      values="Global_active_power", aggfunc="mean")
    st.line_chart(by_daytype, y_label="kW")

left, right = st.columns(2)

with left:
    st.subheader("Average by season")
    season_avg = power.groupby(filtered["Season"]).mean().reindex(SEASON_ORDER).dropna()
    st.bar_chart(season_avg, y_label="kW")

with right:
    st.subheader("Energy share by sub-meter")
    total_wh = power.sum() * 1000 / 60
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
