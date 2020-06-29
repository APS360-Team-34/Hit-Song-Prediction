import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "4c1f5e693ba04424ba05284ea525b427"
client_secret = "57a642672e5f4b0fa9255f38a152b2ad"


def get_spotify_connection():
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return sp