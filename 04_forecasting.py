# Step 4 - forecast next day's average load
# Compare Linear Regression and Random Forest against a simple baseline
# (baseline = "same day last week")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from utils import load_clean_data, save_chart, BLUE, RED

df = load_clean_data()

# convert minute data to daily average
daily = df["Global_active_power"].resample("D").mean().to_frame("load")

# a few days are fully missing, fill them from neighbouring days
print(f"Days with no data: {daily['load'].isna().sum()}")
daily["load"] = daily["load"].interpolate()

# features
daily["lag_1"] = daily["load"].shift(1)      # yesterday
daily["lag_7"] = daily["load"].shift(7)      # same day last week
daily["rolling_7"] = daily["load"].shift(1).rolling(7).mean()   # last 7 days avg
daily["day_of_week"] = daily.index.dayofweek
daily["month"] = daily.index.month
daily = daily.dropna()

features = ["lag_1", "lag_7", "rolling_7", "day_of_week", "month"]
y = daily["load"]

# linear regression needs day/month one hot encoded, random forest doesn't
X_lr = pd.get_dummies(daily[features], columns=["day_of_week", "month"], drop_first=True)
X_rf = daily[features]

# time based split - train on 2007-2009, test on 2010 (no shuffling for time series)
train = daily.index < "2010-01-01"
y_train, y_test = y[train], y[~train]
print(f"Train days: {train.sum()}, Test days: {(~train).sum()}")

lr = LinearRegression()
lr.fit(X_lr[train], y_train)
lr_pred = lr.predict(X_lr[~train])

rf = RandomForestRegressor(n_estimators=300, max_depth=8, random_state=42)
rf.fit(X_rf[train], y_train)
rf_pred = rf.predict(X_rf[~train])

baseline_pred = daily.loc[~train, "lag_7"]


def get_scores(name, actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return {"Model": name, "MAE": round(mae, 3), "RMSE": round(rmse, 3), "MAPE %": round(mape, 1)}


scores = pd.DataFrame([
    get_scores("Baseline (last week)", y_test, baseline_pred),
    get_scores("Linear Regression", y_test, lr_pred),
    get_scores("Random Forest", y_test, rf_pred),
])
scores["Better than baseline %"] = ((1 - scores["MAE"] / scores.loc[0, "MAE"]) * 100).round(1)

print("\n=== Forecast results on 2010 ===")
print(scores.to_string(index=False))

best = scores.loc[scores["MAE"].idxmin(), "Model"]
best_pred = lr_pred if best == "Linear Regression" else rf_pred
print(f"\nBest model: {best}")

# save predictions
results = pd.DataFrame({"actual": y_test,
                        "linear_regression": lr_pred.round(3),
                        "random_forest": rf_pred.round(3)})
results.to_csv("data/forecast_2010.csv")

# ---- actual vs predicted ----
plt.figure(figsize=(14, 5))
plt.plot(y_test.index, y_test.values, label="Actual", color=BLUE, linewidth=1.5)
plt.plot(y_test.index, best_pred, label=f"Predicted ({best})", color=RED, linewidth=1.5, alpha=0.8)
plt.title("Daily Load Forecast - Actual vs Predicted (2010)", fontweight="bold")
plt.ylabel("Average Power (kW)")
plt.legend()
save_chart("7_forecast.png")

# ---- which features matter most (random forest) ----
importance = pd.Series(rf.feature_importances_, index=features).sort_values()

plt.figure(figsize=(8, 4))
plt.barh(importance.index, importance.values, color=BLUE)
plt.title("Feature Importance (Random Forest)", fontweight="bold")
plt.xlabel("Importance")
save_chart("8_feature_importance.png")
