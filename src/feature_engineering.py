import os
from sklearn.preprocessing import MinMaxScaler

from data_loader import load_data
from language import add_language_column

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_vibe(row):
    if row["valence"] < 0.3 and row["energy"] < 0.4:
        return "sad"
    elif row["valence"] > 0.6 and row["energy"] > 0.6:
        return "happy"
    elif row["danceability"] > 0.6:
        return "dance"
    else:
        return "chill"


def process_features():
    df = load_data()

    features = [
        "danceability", "energy", "valence", "tempo",
        "acousticness", "instrumentalness",
        "liveness", "speechiness"
    ]

    df = df.dropna(subset=features)

    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])

    df = add_language_column(df)

    # 🔥 add vibe
    df["vibe"] = df.apply(get_vibe, axis=1)

    save_path = os.path.join(BASE_DIR, "data", "processed_tracks.csv")
    df.to_csv(save_path, index=False)

    print(f"Saved to: {save_path}")

    return df, features, scaler