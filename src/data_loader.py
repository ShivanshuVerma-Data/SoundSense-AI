import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "spotify_tracks.csv")


def load_data():
    df = pd.read_csv(DATA_PATH)

    # remove junk columns safely
    df = df.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], errors="ignore")

    # ensure required columns exist
    required = ["track_name", "artists"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # drop invalid rows
    df = df.dropna(subset=required)

    return df