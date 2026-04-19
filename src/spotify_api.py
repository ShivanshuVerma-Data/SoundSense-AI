import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

# -----------------------------
# 🔥 HARDCODE (DEV ONLY)
# -----------------------------
CLIENT_ID = "edf908cc2b3f4166a537de507d52dd44"
CLIENT_SECRET = "477c39d154c143089877a56b4ce820cf"


def get_spotify_client():
    try:
        auth = SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        return spotipy.Spotify(auth_manager=auth)

    except Exception as e:
        print("Spotify auth failed:", e)
        return None


# -----------------------------
# 🔍 SEARCH SONG
# -----------------------------
def search_song(query):
    sp = get_spotify_client()
    if not sp:
        return None

    try:
        results = sp.search(q=query, type="track", limit=1)
        items = results.get("tracks", {}).get("items", [])

        if not items:
            return None

        track = items[0]

        return {
            "name": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "id": track["id"],
            "preview_url": track.get("preview_url"),
            "image": (
                track.get("album", {})
                     .get("images", [{}])[0]
                     .get("url")
            )
        }

    except Exception as e:
        print("Search failed:", e)
        return None


# -----------------------------
# 🎧 AUDIO FEATURES
# -----------------------------
def get_audio_features(track_id):
    sp = get_spotify_client()
    if not sp:
        return None

    try:
        features = sp.audio_features([track_id])

        if not features or features[0] is None:
            return None

        f = features[0]

        return {
            "danceability": f["danceability"],
            "energy": f["energy"],
            "valence": f["valence"],
            "tempo": f["tempo"],
            "acousticness": f["acousticness"],
            "instrumentalness": f["instrumentalness"],
            "liveness": f["liveness"],
            "speechiness": f["speechiness"]
        }

    except SpotifyException:
        print("Audio features blocked (403). Using fallback.")
        return None

    except Exception as e:
        print("Feature fetch failed:", e)
        return None