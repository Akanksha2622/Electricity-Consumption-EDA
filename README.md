# Electricity Consumption — Exploratory Data Analysis

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pandas](https://img.shields.io/badge/Pandas-EDA-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## Overview

This project is an end-to-end exploratory data analysis of the UCI
Household Electric Power Consumption dataset — 2,075,259 rows of
real electricity readings recorded every minute from 2006 to 2010.

The goal was to clean and process the raw data, identify meaningful
consumption patterns across time, and translate those patterns into
clear, actionable energy efficiency recommendations — the same kind
of work a data analyst would do in an energy or utilities company.

---

## Tools and Technologies

| Tool | Purpose |
|------|---------|
| Python | Core analysis language |
| Pandas | Data cleaning and processing |
| Matplotlib | Charts and visualisations |
| Seaborn | Heatmap and visual styling |
| Google Colab | Notebook environment |

---

## What I Did

- Loaded and explored a 2M+ row real-world dataset
- Handled missing values and converted data types for clean analysis
- Engineered time features — hour, month, season, day type
- Built 6 annotated visualisations to uncover demand patterns
- Derived 3 business recommendations backed by statistical evidence

---

## Key Findings

### Monthly Consumption Trend

![Monthly Trend](Img%201.png)

A clear seasonal cycle is visible throughout the data. Winter months
consistently show 60 to 80 percent higher consumption than summer
months, driven primarily by heating load. The overall average sits
at 1.10 kW across the full four-year period.

---

### Peak Hours of the Day

![Peak Hours](Img%202.png)

Electricity demand peaks at 8 PM every day — the hour when evening
cooking, lighting, and home entertainment all run simultaneously.
The off-peak window between 2 AM and 5 AM uses approximately 75
percent less power than the evening peak.

---

### Weekday vs Weekend Pattern

![Weekday vs Weekend](Img%203.png)

Weekdays show a sharp spike at 7 AM as occupants wake and prepare
for work. This morning surge is completely absent on weekends, where
consumption instead builds gradually through the morning and stays
elevated from 10 AM through 9 PM as people remain at home.

---

### Seasonal Comparison

![Seasonal](Img%204.png)

Winter average consumption (1.41 kW) is nearly double that of
summer (0.72 kW). This gap points to space heating as the single
largest efficiency opportunity in the household energy profile.

---

### Year-on-Year Trend

![Yearly Trend](Img%205.png)

Average consumption fell by 41 percent between 2006 and 2007 and
continued to decline gradually through 2010. This sustained downward
trend suggests the household progressively adopted more
energy-efficient appliances or changed usage behaviour over time.

---

### Correlation Between Measurements

![Correlation Heatmap](Img%206.png)

Sub_metering_3 — which tracks the water heater and air conditioning
unit — shows the strongest correlation with overall consumption at
0.64. Voltage shows a mild negative correlation of -0.40 with power
draw, meaning voltage dips slightly when heavy appliances are running
simultaneously, consistent with known electrical behaviour.

---

## Business Recommendations

Shifting high-power appliances such as washing machines and
dishwashers to the 2 AM to 5 AM off-peak window would meaningfully
reduce strain on the grid during the 8 PM demand spike.

Winter heating represents the highest-impact efficiency opportunity.
Smart thermostat adoption could realistically reduce winter
overconsumption by 15 to 20 percent based on the seasonal gap
observed in this data.

The distinct weekday versus weekend occupancy pattern suggests that
smart home systems could auto-schedule appliances differently on
each day type, improving both cost efficiency and grid stability.

---

## Project Structure

| File | Description |
|------|-------------|
| `electricity_eda.ipynb` | Full analysis notebook |
| `Img 1.png` | Chart — Monthly consumption trend |
| `Img 2.png` | Chart — Peak hours of the day |
| `Img 3.png` | Chart — Weekday vs weekend pattern |
| `Img 4.png` | Chart — Seasonal comparison |
| `Img 5.png` | Chart — Year-on-year trend |
| `Img 6.png` | Chart — Correlation heatmap |
| `README.md` | Project documentation |

---

## How to Run

Clone the repository and install the required libraries:

    git clone https://github.com/Akanksha2622/Electricity-Consumption-EDA.git
    pip install pandas numpy matplotlib seaborn

Open `electricity_eda.ipynb` in Google Colab or Jupyter Notebook
and run the cells sequentially.

---

## Author

Akanksha Kumari
B.Tech Electrical Engineering, IIT Jammu

[![GitHub](https://img.shields.io/badge/GitHub-Akanksha2622-black)](https://github.com/Akanksha2622)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/akanksha-kumari-648ab8309)
