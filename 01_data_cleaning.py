# Step 1 - load the raw data, clean it and add time features
# Dataset: UCI Individual Household Electric Power Consumption

import os
import zipfile
import urllib.request

import pandas as pd

from utils import get_season, CLEAN_FILE

DATA_URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
RAW_FILE = "data/household_power_consumption.txt"

# download the dataset if it's not already there
if not os.path.exists(RAW_FILE):
    os.makedirs("data", exist_ok=True)
    print("Downloading dataset...")
    urllib.request.urlretrieve(DATA_URL, "data/household_power.zip")
    with zipfile.ZipFile("data/household_power.zip") as z:
        z.extractall("data")

# missing values are stored as '?' in this file
df = pd.read_csv(RAW_FILE, sep=";", na_values="?", low_memory=False)

df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d/%m/%Y %H:%M:%S")
df = df.drop(columns=["Date", "Time"])
df = df.set_index("DateTime")

print(f"Dataset size: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Date range: {df.index.min()} to {df.index.max()}")

# ---- missing values ----
print("\nMissing values per column:")
print(df.isna().sum())

missing_rows = df.isna().any(axis=1).sum()
print(f"\nRows with missing values: {missing_rows:,} ({missing_rows / len(df) * 100:.2f}%)")

# every column is empty together in these rows (meter didn't record anything)
# and it's only ~1.25% of the data, so dropping is safer than filling
df = df.dropna()
print(f"Rows after cleaning: {len(df):,}")

# ---- sanity checks ----
print(f"\nDuplicate timestamps: {df.index.duplicated().sum()}")
print(f"Negative power readings: {(df['Global_active_power'] < 0).sum()}")
print(f"Voltage range: {df['Voltage'].min()} - {df['Voltage'].max()} V")

# ---- feature engineering ----
df["Year"] = df.index.year
df["Month"] = df.index.month
df["Hour"] = df.index.hour
df["DayOfWeek"] = df.index.dayofweek
df["DayType"] = df["DayOfWeek"].apply(lambda d: "Weekend" if d >= 5 else "Weekday")
df["Season"] = df["Month"].apply(get_season)

print("\nNew columns added: Year, Month, Hour, DayOfWeek, DayType, Season")
print(df.head())

df.to_csv(CLEAN_FILE)
print(f"\nSaved cleaned data to {CLEAN_FILE}")

# ---- smaller hourly file for the Streamlit app ----
# the minute-level file is too big for GitHub, so the dashboard uses hourly totals.
# keeping energy + minute counts (not averages) so the app's numbers match exactly
power = df["Global_active_power"]
hourly = pd.DataFrame({
    "Energy_kWh": (power / 60).resample("h").sum(),
    "Minutes": power.resample("h").count(),
    "Max_power": power.resample("h").max(),
    "Sub_metering_1": df["Sub_metering_1"].resample("h").sum(),
    "Sub_metering_2": df["Sub_metering_2"].resample("h").sum(),
    "Sub_metering_3": df["Sub_metering_3"].resample("h").sum(),
})
hourly = hourly[hourly["Minutes"] > 0]

hourly["Year"] = hourly.index.year
hourly["Hour"] = hourly.index.hour
hourly["DayType"] = hourly.index.dayofweek.map(lambda d: "Weekend" if d >= 5 else "Weekday")
hourly["Season"] = hourly.index.month.map(get_season)

hourly.round(4).to_csv("data/hourly_data.csv")
print(f"Saved hourly data for the dashboard: {len(hourly):,} rows")
