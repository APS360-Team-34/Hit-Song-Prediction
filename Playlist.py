import json
import pickle
import pandas as pd
import numpy as np
from DataProcessing import normalize_dataframe


def save_playlist(playlist, file=None):
    """
    Saves playlist object into a pickle
    :param file: Name of file to save into (default - playlist_[ID])
    :return: Name of file that was saved into
    """
    file = f"playlist_{playlist.id}" if file is None else file
    with open(file, 'wb') as f:
        pickle.dump(playlist, f)

    print(f"Saved playlist into file: {file}")
    return file

def load_playlist(file):
    """
    Saves playlist object into a pickle
    :param file: Name of file to load from
    :return: Object that was loaded
    """
    with open(file, 'rb') as f:
        playlist = pickle.load(f)

    print(f"Loaded playlist from file: {file}")
    return playlist


class Playlist:
    def __init__(self, playlist_id):
        self.id = playlist_id
        self.playlist_track_ids = []
        self.playlist_df = None

    def load_playlist_tracks(self, sp):
        """
        Loads Playlist object with track ids
        :param sp: Spotify Connection
        :return: List of loaded track ids
        """
        print(f"Loading playlist {self.id} tracks...")

        results = sp.playlist_tracks(self.id)

        while results['next']:
            for i in results['items']:
                track = i['track']
                if track['id']:
                    self.playlist_track_ids.append(track['id'])
            results = sp.next(results)

        print(f"Done.")

        return self.playlist_track_ids

    def get_playlist_tracks(self):
        """
        Return loaded playlist track ids
        :return: List of loaded playlist track ids
        """
        return self.playlist_track_ids

    def save_playlist_tracks(self, file=None):
        """
        Saves playlist track ids into a json file
        :param file: Name of file to save into (default - playlist_[ID]_tracks.json)
        :return: Name of the file that was saved into
        """
        file = f"playlist_{self.id}_tracks.json" if file is None else file

        with open(file, 'w') as f:
            json.dump(self.playlist_track_ids, f, indent=2)

        return file


    def load_playlist_df(self, sp):
        """
        Populates a df with information about the playlist tracks
        :param sp: Spotify connection
        :return: DataFrame with information on playlist tracks
        """
        print(f"Loading playlist {self.id} track information into DataFrame...")
        playlist_track_features = []

        for i in range(0, len(self.playlist_track_ids), 50):
            tracks_info = sp.tracks(self.playlist_track_ids[i: i + 50])['tracks']
            tracks_features = sp.audio_features(self.playlist_track_ids[i:i+50])
            for k, track in enumerate(tracks_info):
                if track:
                    playlist_track_features.append({
                        'id': track['id'],
                        'name': track['name'],
                        'popularity': track['popularity'],
                        'duration': track['duration_ms'],
                        'key': tracks_features[k]['key'],
                        'mode': tracks_features[k]['mode'],
                        'time_signature': tracks_features[k]['time_signature'],
                        'acousticness': tracks_features[k]['acousticness'],
                        'danceability': tracks_features[k]['danceability'],
                        'energy': tracks_features[k]['energy'],
                        'instrumentalness': tracks_features[k]['instrumentalness'],
                        'liveness': tracks_features[k]['liveness'],
                        'loudness': tracks_features[k]['loudness'],
                        'speechiness': tracks_features[k]['speechiness'],
                        'valence': tracks_features[k]['valence'],
                        'tempo': tracks_features[k]['tempo']
                    })

        self.playlist_df = pd.DataFrame(playlist_track_features)
        print(f"Done.")

        return self.playlist_df

    def get_playlist_df(self, cols=None):
        """
        Return loaded playlist dataframe
        :return: DataFrame with information on playlist tracks
        """
        return self.playlist_df[cols] if cols else self.playlist_df
