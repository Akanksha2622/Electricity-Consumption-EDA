# Step 2 - exploratory analysis, 6 charts and a summary dashboard image

import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_clean_data, save_chart, SEASON_ORDER, BLUE, RED

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams["font.size"] = 12

df = load_clean_data()
power = df["Global_active_power"]

# ---- summary stats ----
print("=== Electricity Consumption Summary ===")
print(f"Average power used: {power.mean():.3f} kW")
print(f"Maximum power used: {power.max():.3f} kW")
print(f"Minimum power used: {power.min():.3f} kW")

daily_avg = power.resample("D").mean()
monthly_avg = power.resample("ME").mean()
print(f"Highest daily average: {daily_avg.max():.3f} kW")
print(f"Lowest daily average: {daily_avg.min():.3f} kW")


# ---- Chart 1: monthly trend ----
plt.figure(figsize=(14, 5))
monthly_avg.plot(color=BLUE, linewidth=2)
plt.axhline(monthly_avg.mean(), color=RED, linestyle="--",
            label=f"Overall average: {monthly_avg.mean():.2f} kW")
plt.title("Monthly Average Electricity Consumption (2006-2010)", fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Average Power (kW)")
plt.legend()
save_chart("1_monthly_trend.png")


# ---- Chart 2: peak hour ----
hourly_avg = power.groupby(df["Hour"]).mean()
peak_hour = hourly_avg.idxmax()
colors = [RED if h == peak_hour else BLUE for h in hourly_avg.index]

plt.figure(figsize=(12, 5))
plt.bar(hourly_avg.index, hourly_avg.values, color=colors)
plt.title("Average Electricity Use by Hour of Day", fontweight="bold")
plt.xlabel("Hour of Day")
plt.ylabel("Average Power (kW)")
plt.xticks(range(24))
save_chart("2_peak_hours.png")

night_avg = hourly_avg.loc[1:5].mean()
print(f"\nPeak hour: {peak_hour}:00 ({hourly_avg.max():.3f} kW)")
print(f"Night time (1-5 AM) average: {night_avg:.3f} kW")


# ---- Chart 3: weekday vs weekend ----
weekday = df[df["DayType"] == "Weekday"].groupby("Hour")["Global_active_power"].mean()
weekend = df[df["DayType"] == "Weekend"].groupby("Hour")["Global_active_power"].mean()

plt.figure(figsize=(12, 5))
plt.plot(weekday.index, weekday.values, label="Weekday", color=BLUE, linewidth=2.5)
plt.plot(weekend.index, weekend.values, label="Weekend", color=RED, linewidth=2.5)
plt.title("Weekday vs Weekend Hourly Consumption", fontweight="bold")
plt.xlabel("Hour of Day")
plt.ylabel("Average Power (kW)")
plt.xticks(range(24))
plt.legend()
save_chart("3_weekday_vs_weekend.png")

daytype_avg = power.groupby(df["DayType"]).mean()
print(f"\nWeekday average: {daytype_avg['Weekday']:.3f} kW")
print(f"Weekend average: {daytype_avg['Weekend']:.3f} kW")


# ---- Chart 4: seasons ----
season_avg = power.groupby(df["Season"]).mean()[SEASON_ORDER]

plt.figure(figsize=(8, 5))
plt.bar(SEASON_ORDER, season_avg.values, color=["#3498db", "#2ecc71", "#f39c12", "#e67e22"], width=0.5)
plt.title("Average Consumption by Season", fontweight="bold")
plt.ylabel("Average Power (kW)")
save_chart("4_seasonal.png")

print("\nSeason averages:")
print(season_avg.round(3))
print(f"Winter vs Summer: {season_avg['Winter'] / season_avg['Summer']:.2f}x")


# ---- Chart 5: yearly trend ----
# note: 2006 only has the last 2 weeks of December so it looks high
yearly_avg = power.groupby(df["Year"]).mean()

plt.figure(figsize=(8, 5))
plt.plot(yearly_avg.index, yearly_avg.values, marker="o", markersize=10, color=BLUE, linewidth=2.5)
for year, val in yearly_avg.items():
    plt.annotate(f"{val:.2f}", (year, val), textcoords="offset points", xytext=(0, 10), ha="center")
plt.title("Yearly Average Consumption", fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Average Power (kW)")
plt.xticks(yearly_avg.index)
save_chart("5_yearly_trend.png")


# ---- Chart 6: correlation heatmap ----
cols = ["Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity",
        "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]

plt.figure(figsize=(9, 7))
sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Between Measurements", fontweight="bold")
save_chart("6_correlation.png")


# ---- which appliances use the most energy ----
# sub meters are in watt-hours per minute, global active power is in kW
total_energy = (power * 1000 / 60).sum()
kitchen = df["Sub_metering_1"].sum() / total_energy * 100
laundry = df["Sub_metering_2"].sum() / total_energy * 100
heater_ac = df["Sub_metering_3"].sum() / total_energy * 100
other = 100 - kitchen - laundry - heater_ac

print("\nShare of total energy:")
print(f"Kitchen: {kitchen:.1f}%")
print(f"Laundry: {laundry:.1f}%")
print(f"Water heater & AC: {heater_ac:.1f}%")
print(f"Other (not sub-metered): {other:.1f}%")


# ---- Dashboard: key charts on one page ----
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

monthly_avg.plot(ax=axes[0, 0], color=BLUE, linewidth=2)
axes[0, 0].set_title("Monthly Trend")
axes[0, 0].set_ylabel("kW")

axes[0, 1].bar(hourly_avg.index, hourly_avg.values, color=colors)
axes[0, 1].set_title(f"Hourly Pattern (peak at {peak_hour}:00)")
axes[0, 1].set_xlabel("Hour")

axes[1, 0].plot(weekday.index, weekday.values, label="Weekday", color=BLUE, linewidth=2)
axes[1, 0].plot(weekend.index, weekend.values, label="Weekend", color=RED, linewidth=2)
axes[1, 0].set_title("Weekday vs Weekend")
axes[1, 0].set_xlabel("Hour")
axes[1, 0].set_ylabel("kW")
axes[1, 0].legend()

axes[1, 1].pie([kitchen, laundry, heater_ac, other],
               labels=["Kitchen", "Laundry", "Water heater & AC", "Other"],
               autopct="%1.0f%%", colors=["#2ecc71", "#f39c12", RED, "#bdc3c7"])
axes[1, 1].set_title("Energy Share by Sub-meter")

fig.suptitle(f"Household Electricity Dashboard  |  Avg {power.mean():.2f} kW  |  "
             f"Peak {peak_hour}:00  |  Winter {season_avg['Winter']:.2f} kW vs Summer {season_avg['Summer']:.2f} kW",
             fontsize=15, fontweight="bold")
save_chart("dashboard.png")
