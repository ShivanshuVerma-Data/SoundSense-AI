import os
import sys
import pandas as pd
import streamlit as st
from rapidfuzz import process

# -----------------------------
# Fix imports
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_PATH)

from recommender import recommend
from explain import explain_recommendation
from spotify_helper import search_track


# -----------------------------
# Load data (cached)
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, "data", "processed_tracks.csv"))

df = load_data()


# -----------------------------
# Cache Spotify calls
# -----------------------------
@st.cache_data
def get_track_assets(name, artist):
    return search_track(name, artist)


# -----------------------------
# UI Config
# -----------------------------
st.set_page_config(page_title="SoundSense AI", layout="wide")


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #ffffff;
}

.subtitle {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 30px;
}

.card {
    background-color: #1c1f26;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.song-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
}

.song-artist {
    font-size: 14px;
    color: #9ca3af;
}

.section {
    margin-top: 30px;
    margin-bottom: 10px;
    font-size: 22px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="title">SoundSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Music Recommendation System</div>', unsafe_allow_html=True)


# -----------------------------
# Search
# -----------------------------
query = st.text_input("Search for a song")

selected_song = None

if query:
    results = process.extract(query, df["track_name"].tolist(), limit=5)
    indices = [r[2] for r in results]
    matches = df.iloc[indices]

    options = [
        f"{row['track_name']} — {row['artists']}"
        for _, row in matches.iterrows()
    ]

    choice = st.selectbox("Select a song", options)
    selected_song = matches.iloc[options.index(choice)]


# -----------------------------
# Display selected + recommend
# -----------------------------
if selected_song is not None:

    st.markdown('<div class="section">Selected Song</div>', unsafe_allow_html=True)

    image, preview = get_track_assets(
        selected_song["track_name"],
        selected_song["artists"]
    )

    st.markdown(f"""
    <div class="card">
        <div class="song-title">{selected_song['track_name']}</div>
        <div class="song-artist">{selected_song['artists']}</div>
    </div>
    """, unsafe_allow_html=True)

    if image:
        st.image(image, width=300)

    if preview:
        st.audio(preview)

    # -----------------------------
    # Recommendations
    # -----------------------------
    recs = recommend(selected_song.to_dict(), df)

    st.markdown('<div class="section">Recommended Songs</div>', unsafe_allow_html=True)

    for _, row in recs.iterrows():

        image, preview = get_track_assets(
            row["track_name"],
            row["artists"]
        )

        st.markdown(f"""
        <div class="card">
            <div class="song-title">{row['track_name']}</div>
            <div class="song-artist">{row['artists']}</div>
        </div>
        """, unsafe_allow_html=True)

        if image:
            st.image(image, width=250)

        if preview:
            st.audio(preview)

        reasons = explain_recommendation(selected_song, row)

        for r in reasons:
            st.write(f"- {r}")