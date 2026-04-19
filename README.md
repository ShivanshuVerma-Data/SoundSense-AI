# SoundSense AI

SoundSense AI is an intelligent music recommendation system that suggests songs based on audio features, mood similarity, and contextual ranking. It combines machine learning techniques with a clean web interface to deliver relevant and consistent music recommendations.

---

## Live Demo

Add your deployed app link here after deployment.

---

## Features

- Smart search with fuzzy matching  
- Audio feature-based recommendation using machine learning  
- Context-aware ranking (similarity, popularity, artist relevance)  
- Mood and energy-based filtering  
- Language-aware recommendations  
- Explainable results (why a song was recommended)  
- Interactive web interface built with Streamlit  
- Album artwork and audio preview via Spotify API  

---

## Tech Stack

- Python  
- Pandas  
- Scikit-learn  
- Streamlit  
- RapidFuzz  
- Spotipy (Spotify Web API)  

---

## Project Structure

```
SoundSense-AI/
│
├── app/                 # Streamlit application
├── src/                 # Core logic (recommender, preprocessing, helpers)
├── data/                # Processed dataset
├── outputs/             # Saved models (optional)
├── requirements.txt     # Dependencies
└── README.md
```

---




## Installation and Setup

Clone the repository:

bash
git clone https://github.com/YOUR_USERNAME/SoundSense-AI.git
cd SoundSense-AI

pip install -r requirements.txt
streamlit run app/app.py

---

## Environment Variables

Set the following environment variables for Spotify integration:

SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret

For deployment (e.g., Streamlit Cloud), add these in the app’s Secrets configuration.

---

## How It Works

Uses K-Nearest Neighbors (KNN) for similarity-based retrieval
Applies dynamic feature weighting based on song characteristics
Filters candidates using mood, energy, and language constraints
Ranks results using a combination of:
similarity score
popularity
artist relevance
Applies diversity (MMR) to avoid repetitive recommendations

---

## Screenshots : 

<img width="885" height="405" alt="image" src="https://github.com/user-attachments/assets/d50364d3-5400-4980-92f4-32cee337c827" />

<img width="888" height="735" alt="image" src="https://github.com/user-attachments/assets/2205bae8-8743-49c4-af05-dc1dd350f77c" />

---

## Future Improvements

User personalization and listening history
Playlist generation
Enhanced mood detection using NLP
Mobile-optimized interface

---
