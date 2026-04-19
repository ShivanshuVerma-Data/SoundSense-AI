import numpy as np
from sklearn.neighbors import NearestNeighbors

FEATURES = [
    "danceability", "energy", "valence", "tempo",
    "acousticness", "instrumentalness",
    "liveness", "speechiness"
]


# Build KNN model
def build_knn(df):
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(df[FEATURES].values)
    return model


# Assign feature weights based on song characteristics
def get_feature_weights(song):
    weights = {f: 1.0 for f in FEATURES}

    if song["valence"] < 0.35:
        weights["valence"] = 2.3
        weights["energy"] = 1.5

    if song["valence"] > 0.7:
        weights["valence"] = 2.0

    if song["energy"] > 0.7:
        weights["energy"] = 2.0

    if song["danceability"] > 0.7:
        weights["danceability"] = 2.0

    if song["acousticness"] > 0.6:
        weights["acousticness"] = 1.8

    return weights


# Compute weighted distance between two songs
def weighted_distance(a, b, weights):
    return np.mean([
        abs(a[f] - b[f]) * weights[f] for f in FEATURES
    ])


# Select diverse results using MMR
def mmr_select(candidates, df, k=5, lambda_=0.8):
    selected = []

    while candidates and len(selected) < k:
        best = None
        best_score = -1

        for idx, base_score in candidates:
            diversity_penalty = 0

            for s_idx in selected:
                sim = 1 - np.mean([
                    abs(df.loc[idx][f] - df.loc[s_idx][f])
                    for f in FEATURES
                ])
                diversity_penalty = max(diversity_penalty, sim)

            score = lambda_ * base_score - (1 - lambda_) * diversity_penalty

            if score > best_score:
                best_score = score
                best = idx

        selected.append(best)
        candidates = [(i, s) for i, s in candidates if i != best]

    return selected


# Main recommendation function
def recommend(song_features, df, top_n=5):
    base_name = str(song_features.get("track_name", "")).lower()
    base_artist = str(song_features.get("artists", "")).split(",")[0].lower()
    base_lang = song_features.get("lang", "en")

    pool = df[df["lang"] == base_lang]

    if len(pool) < 50:
        pool = df

    weights = get_feature_weights(song_features)

    model = build_knn(pool)
    query = np.array([song_features[f] for f in FEATURES]).reshape(1, -1)

    distances, indices = model.kneighbors(query, n_neighbors=100)

    candidates = []
    seen = set()

    for dist, i in zip(distances[0], indices[0]):
        row = pool.iloc[i]
        name = row["track_name"].lower()

        if name == base_name or name in seen:
            continue

        if abs(song_features["valence"] - row["valence"]) > 0.20:
            continue

        if abs(song_features["energy"] - row["energy"]) > 0.20:
            continue

        sim = 1 - weighted_distance(song_features, row, weights)

        if sim < 0.65:
            continue

        pop = row["popularity"] / 100

        artist = 1 if base_artist in row["artists"].lower() else 0

        score = (
            sim * 0.55 +
            pop * 0.25 +
            artist * 0.20
        )

        candidates.append((pool.index[i], score))
        seen.add(name)

    candidates = sorted(candidates, key=lambda x: x[1], reverse=True)

    selected_indices = mmr_select(candidates, df, k=top_n)

    return df.loc[selected_indices]