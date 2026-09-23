# helper functions used by the other scripts

import os

import pandas as pd
import matplotlib.pyplot as plt

CLEAN_FILE = "data/cleaned_data.csv"
IMAGE_DIR = "images"

SEASON_ORDER = ["Winter", "Spring", "Summer", "Autumn"]
BLUE = "#1a6fd4"
RED = "#e74c3c"


def load_clean_data():
    if not os.path.exists(CLEAN_FILE):
        raise FileNotFoundError("cleaned_data.csv not found - run 01_data_cleaning.py first")
    return pd.read_csv(CLEAN_FILE, index_col="DateTime", parse_dates=True)


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"


def save_chart(filename):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(f"{IMAGE_DIR}/{filename}", dpi=150)
    plt.close()
    print(f"Saved {IMAGE_DIR}/{filename}")
