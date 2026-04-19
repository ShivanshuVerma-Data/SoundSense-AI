import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"


def get_client():
    auth = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return spotipy.Spotify(auth_manager=auth)


sp = get_client()


def search_track(name, artist):
    query = f"{name} {artist}"

    try:
        results = sp.search(q=query, type="track", limit=1)

        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]

            image = track["album"]["images"][0]["url"] if track["album"]["images"] else None
            preview = track["preview_url"]

            return image, preview

    except:
        pass

    return None, None