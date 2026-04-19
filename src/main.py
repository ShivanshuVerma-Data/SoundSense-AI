import os
import pandas as pd

from recommender import recommend
from explain import explain_recommendation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# -----------------------------
#  SEARCH SONGS
# -----------------------------
from rapidfuzz import process

def search_songs(df, query, limit=5):
    choices = df["track_name"].tolist()

    results = process.extract(query, choices, limit=limit)

    indices = [r[2] for r in results]

    return df.iloc[indices].sort_values(by="popularity", ascending=False)


# -----------------------------
#  SELECT SONG
# -----------------------------
def select_song(matches):
    print("\nSelect a song:\n")

    for i, (_, row) in enumerate(matches.iterrows(), 1):
        print(f"{i}. {row['track_name']} — {row['artists']}")

    while True:
        try:
            choice = int(input("\nEnter number: "))
            if 1 <= choice <= len(matches):
                return matches.iloc[choice - 1]
        except:
            pass

        print("Invalid choice, try again.")


# -----------------------------
#  MAIN
# -----------------------------
def main():
    print("Loading system...\n")

    df = pd.read_csv(os.path.join(BASE_DIR, "data", "processed_tracks.csv"))

    #  USER INPUT
    query = input("Search for a song: ")

    print("\nSearching...\n")

    matches = search_songs(df, query)

    if matches is None:
        print("No songs found.")
        return

    #  USER SELECTS SONG
    song = select_song(matches)

    print(f"\nSelected: {song['track_name']} — {song['artists']}\n")

    #  RECOMMEND
    recs = recommend(song.to_dict(), df)

    print("\nRecommended Songs:\n")

    for i, (_, row) in enumerate(recs.iterrows(), 1):
        print(f"{i}. {row['track_name']} — {row['artists']}")

    print("\nWhy these songs:\n")

    for i, (_, row) in enumerate(recs.iterrows(), 1):
        print(f"{i}. {row['track_name']}")
        for r in explain_recommendation(song, row):
            print("   -", r)
        print()


# -----------------------------
if __name__ == "__main__":
    main()