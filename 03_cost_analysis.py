# Step 3 - estimate the yearly electricity bill and how much the
# recommendations could save, using a peak / off-peak tariff
#
# Tariff assumption (French EDF "Heures Creuses" plan, approx):
#   off-peak 10 PM - 6 AM  -> 0.21 EUR/kWh
#   peak     6 AM - 10 PM  -> 0.27 EUR/kWh

import matplotlib.pyplot as plt
from utils import load_clean_data, save_chart, BLUE, RED

PEAK_PRICE = 0.27
OFFPEAK_PRICE = 0.21

df = load_clean_data()

# use only full years so the yearly numbers are fair
df = df[(df["Year"] >= 2007) & (df["Year"] <= 2009)]
n_years = 3

df["kWh"] = df["Global_active_power"] / 60      # kW for 1 minute -> kWh
df["OffPeak"] = (df["Hour"] >= 22) | (df["Hour"] < 6)

peak_kwh = df.loc[~df["OffPeak"], "kWh"].sum() / n_years
offpeak_kwh = df.loc[df["OffPeak"], "kWh"].sum() / n_years
yearly_bill = peak_kwh * PEAK_PRICE + offpeak_kwh * OFFPEAK_PRICE

print("=== Yearly usage & bill (avg of 2007-2009) ===")
print(f"Total usage: {peak_kwh + offpeak_kwh:,.0f} kWh/year")
print(f"Used in off-peak hours: {offpeak_kwh / (peak_kwh + offpeak_kwh) * 100:.1f}%")
print(f"Estimated bill: {yearly_bill:,.0f} EUR/year")

# ---- savings if loads are moved to off-peak hours ----
price_diff = PEAK_PRICE - OFFPEAK_PRICE

# 1. water heater (sub meter 3) heating at night instead of during the day
heater_peak_kwh = df.loc[~df["OffPeak"], "Sub_metering_3"].sum() / 1000 / n_years
heater_saving = heater_peak_kwh * price_diff

# 2. dishwasher / washing machine / dryer (sub meters 1 & 2) run after 10 PM instead of 6-10 PM
evening = (df["Hour"] >= 18) & (df["Hour"] < 22)
appliance_kwh = df.loc[evening, ["Sub_metering_1", "Sub_metering_2"]].sum().sum() / 1000 / n_years
appliance_saving = appliance_kwh * price_diff

total_saving = heater_saving + appliance_saving

print("\n=== Possible savings ===")
print(f"Water heater on night timer: {heater_peak_kwh:,.0f} kWh shifted -> {heater_saving:,.0f} EUR/year")
print(f"Kitchen & laundry after 10 PM: {appliance_kwh:,.0f} kWh shifted -> {appliance_saving:,.0f} EUR/year")
print(f"Total: {total_saving:,.0f} EUR/year ({total_saving / yearly_bill * 100:.1f}% of the bill)")

# ---- chart: current vs after shifting ----
after_bill = yearly_bill - total_saving

plt.figure(figsize=(7, 5))
bars = plt.bar(["Current", "After shifting loads"], [yearly_bill, after_bill], color=[RED, BLUE], width=0.5)
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 20,
             f"{bar.get_height():,.0f} EUR", ha="center", fontsize=12)
plt.title("Estimated Yearly Electricity Bill", fontweight="bold")
plt.ylabel("EUR / year")
plt.ylim(0, yearly_bill * 1.15)
save_chart("9_cost_savings.png")
