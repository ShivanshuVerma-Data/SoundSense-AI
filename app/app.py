import os
import sys
import pandas as pd
import streamlit as st
from rapidfuzz import process

# -----------------------------
# Imports
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_PATH)

from recommender import recommend
from explain import explain_recommendation
from spotify_helper import search_track

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE_DIR, "data", "processed_tracks.csv"))

df = load_data()

# -----------------------------
# Spotify cache
# -----------------------------
@st.cache_data
def get_track_assets(name, artist):
    return search_track(name, artist)

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="SoundSense AI", layout="wide")

# -----------------------------
# PREMIUM CSS
# -----------------------------
st.markdown("""
<style>

/* Global */
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* Title */
.title {
    font-size: 46px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}

/* Section */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 40px;
    margin-bottom: 15px;
}

/* Cards */
.card {
    background: #15181f;
    padding: 16px;
    border-radius: 14px;
    transition: all 0.2s ease;
    border: 1px solid rgba(255,255,255,0.05);
}

.card:hover {
    transform: translateY(-4px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Selected song highlight */
.now-playing {
    background: linear-gradient(135deg, #1f2937, #111827);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 16px;
}

/* Text */
.song-title {
    font-size: 16px;
    font-weight: 600;
}

.song-artist {
    font-size: 13px;
    color: #9ca3af;
}

/* Footer */
.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="title">SoundSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover music based on mood, vibe, and similarity</div>', unsafe_allow_html=True)

# -----------------------------
# Search (centered)
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    query = st.text_input("", placeholder="Search for a song...")

selected_song = None

# -----------------------------
# Search logic
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
# Selected song
# -----------------------------
if selected_song is not None:

    st.markdown('<div class="section-title">Now Playing</div>', unsafe_allow_html=True)

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
        <div class="now-playing">
            <div class="song-title" style="font-size:22px;">
                {selected_song['track_name']}
            </div>
            <div class="song-artist">
                {selected_song['artists']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if preview:
            st.audio(preview)

# -----------------------------
# Recommendations
# -----------------------------
    st.markdown('<div class="section-title">Recommended for You</div>', unsafe_allow_html=True)

    recs = recommend(selected_song.to_dict(), df)

    for i in range(0, len(recs), 3):
        cols = st.columns(3)

        for j in range(3):
            if i + j >= len(recs):
                break

            row = recs.iloc[i + j]

            image, preview = get_track_assets(
                row["track_name"],
                row["artists"]
            )

            with cols[j]:
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

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    '<div class="footer">SoundSense AI • Smart music recommendations</div>',
    unsafe_allow_html=True
)