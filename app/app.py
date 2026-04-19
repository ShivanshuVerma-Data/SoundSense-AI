import os
import sys
import pandas as pd
import streamlit as st
from rapidfuzz import process

# -----------------------------
# Fix imports (important for Streamlit Cloud)
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
# Cache Spotify API calls
# -----------------------------
@st.cache_data
def get_track_assets(name, artist):
    return search_track(name, artist)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="SoundSense AI",
    page_icon="🎧",
    layout="wide"
)

# -----------------------------
# Custom UI Styling
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.title {
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
}

.subtitle {
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 30px;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 10px;
}

.card {
    background: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    transition: 0.2s ease-in-out;
}

.card:hover {
    background: #2a2f3a;
}

.song-title {
    font-size: 18px;
    font-weight: 600;
}

.song-artist {
    font-size: 14px;
    color: #9ca3af;
}

.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="title">SoundSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover music based on mood, vibe, and similarity</div>', unsafe_allow_html=True)

st.divider()

# -----------------------------
# Centered Search
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    query = st.text_input("Search for a song", placeholder="Try: Sukoon Mila")

selected_song = None

# -----------------------------
# Search Logic
# -----------------------------
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
# Selected Song Section
# -----------------------------
if selected_song is not None:

    st.markdown('<div class="section-title">Selected Song</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    image, preview = get_track_assets(
        selected_song["track_name"],
        selected_song["artists"]
    )

    with col1:
        if image:
            st.image(image, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="song-title">{selected_song['track_name']}</div>
            <div class="song-artist">{selected_song['artists']}</div>
        </div>
        """, unsafe_allow_html=True)

        if preview:
            st.audio(preview)

# -----------------------------
# Recommendations Section
# -----------------------------
    st.markdown('<div class="section-title">Recommended Songs</div>', unsafe_allow_html=True)

    recs = recommend(selected_song.to_dict(), df)

    cols = st.columns(3)

    for i, (_, row) in enumerate(recs.iterrows()):
        image, preview = get_track_assets(
            row["track_name"],
            row["artists"]
        )

        with cols[i % 3]:
            if image:
                st.image(image, use_container_width=True)

            st.markdown(f"""
            <div class="card">
                <div class="song-title">{row['track_name']}</div>
                <div class="song-artist">{row['artists']}</div>
            </div>
            """, unsafe_allow_html=True)

            if preview:
                st.audio(preview)

            reasons = explain_recommendation(selected_song, row)

            for r in reasons:
                st.caption(f"• {r}")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.markdown(
    '<div class="center">Built with Machine Learning • SoundSense AI</div>',
    unsafe_allow_html=True
)