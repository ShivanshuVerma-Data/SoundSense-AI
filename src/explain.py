FEATURES = {
    "danceability": "groove",
    "energy": "intensity",
    "valence": "mood",
    "tempo": "speed",
    "acousticness": "acoustic feel",
    "instrumentalness": "instrumental nature",
    "liveness": "live performance feel",
    "speechiness": "spoken/rap content"
}

# priority features that matter most to listeners
PRIORITY = ["valence", "energy", "danceability"]


def explain_recommendation(song_row, rec_row):
    scored = []

    # collect features that are reasonably close
    for feature, meaning in FEATURES.items():
        diff = abs(song_row[feature] - rec_row[feature])

        if diff < 0.1:
            scored.append((feature, diff, meaning))

    # sort by similarity (lower diff first)
    scored.sort(key=lambda x: x[1])

    explanation = []

    # step 1: add priority features first (mood, energy, groove)
    for feature, diff, meaning in scored:
        if feature in PRIORITY:
            explanation.append(f"Similar {meaning}")

    # step 2: if no priority feature matched strongly, allow relaxed threshold
    if not explanation:
        for feature in PRIORITY:
            diff = abs(song_row[feature] - rec_row[feature])
            if diff < 0.2:
                explanation.append(f"Similar {FEATURES[feature]}")
                break

    # step 3: fill remaining slots (max 3 total)
    for feature, diff, meaning in scored:
        if len(explanation) >= 3:
            break
        if f"Similar {meaning}" not in explanation:
            explanation.append(f"Similar {meaning}")

    # step 4: ensure at least one human-friendly reason (mood/intensity/groove)
    human_keywords = ["mood", "intensity", "groove"]

    if not any(any(k in exp for k in human_keywords) for exp in explanation):
        for feature in PRIORITY:
            diff = abs(song_row[feature] - rec_row[feature])
            if diff < 0.2:
                explanation.insert(0, f"Similar {FEATURES[feature]}")
                break

    # fallback if nothing matched
    if not explanation:
        explanation.append("Overall similar sound profile")

    return explanation[:3]