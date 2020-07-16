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
        self.playlist_artists = {}

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

        for i in results['items']:
            track = i['track']
            if track['id']:
                self.playlist_track_ids.append(track['id'])

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


    def get_max_artist_popularity(self, sp, artists):
        """
        Returns maximum artist popularity of track
        :param sp: Spotify connection
        :param artists: Artists information from track
        :return: Maximum popularity of artists
        """
        artist_ids = []
        for artist in artists:
            artist_ids.append(artist['id'])

        try:
            artist_info = sp.artists(artist_ids)['artists']
            popularities = []
            for artist in artist_info:
                popularities.append(artist['popularity'])

            max_popularity = np.array(popularities).max()
            return max_popularity
        except:
            return None

    def get_artists_top_tracks_avg_popularity(self, sp, artists):
        """
        Returns maximum artist popularity of track
        :param sp: Spotify connection
        :param artists: Artists information from track
        :return: Maximum popularity of artists
        """
        artist_ids = []
        for artist in artists:
            artist_ids.append(artist['id'])

        try:
            popularities = []
            for artist in artist_ids:
                top_tracks = sp.artist_top_tracks(artist, country='US')
                for track in top_tracks['tracks']:
                    popularities.append(track['popularity'])

            avg_popularity = np.array(popularities).mean()
            return avg_popularity
        except:
            return None

    ''' Deprecated '''
    # def load_playlist_df(self, sp):
    #     """
    #     Populates a df with information about the playlist tracks
    #     :param sp: Spotify connection
    #     :return: DataFrame with information on playlist tracks
    #     """
    #     print(f"Loading playlist {self.id} track information into DataFrame...")
    #     playlist_track_features = []
    #
    #     for i in range(0, len(self.playlist_track_ids), 50):
    #         try:
    #             tracks_info = sp.tracks(self.playlist_track_ids[i: i + 50])['tracks']
    #             tracks_features = sp.audio_features(self.playlist_track_ids[i:i+50])
    #             for k, track in enumerate(tracks_info):
    #                 print(i + k)
    #                 if track:
    #                     artists = track['artists']
    #
    #                     playlist_track_features.append({
    #                         'id': track['id'],
    #                         'name': track['name'],
    #                         'popularity': track['popularity'],
    #                         'duration': track['duration_ms'],
    #                         'key': tracks_features[k]['key'],
    #                         'mode': tracks_features[k]['mode'],
    #                         'time_signature': tracks_features[k]['time_signature'],
    #                         'acousticness': tracks_features[k]['acousticness'],
    #                         'danceability': tracks_features[k]['danceability'],
    #                         'energy': tracks_features[k]['energy'],
    #                         'instrumentalness': tracks_features[k]['instrumentalness'],
    #                         'liveness': tracks_features[k]['liveness'],
    #                         'loudness': tracks_features[k]['loudness'],
    #                         'speechiness': tracks_features[k]['speechiness'],
    #                         'valence': tracks_features[k]['valence'],
    #                         'tempo': tracks_features[k]['tempo'],
    #                         'max_artist_popularity': self.get_max_artist_popularity(sp, artists),
    #                         'avg_popularity_artist_top_tracks': self.get_artists_top_tracks_avg_popularity(sp, artists),
    #                         'release_date': track['album']['release_date'],
    #                         'explicit': track['explicit']
    #                     })
    #         except:
    #             pass
    #
    #     self.playlist_df = pd.DataFrame(playlist_track_features)
    #     print(f"Done.")
    #
    #     return self.playlist_df
    #
    # def get_playlist_df(self, cols=None):
    #     """
    #     Return loaded playlist dataframe
    #     :return: DataFrame with information on playlist tracks
    #     """
    #     return self.playlist_df[cols] if cols else self.playlist_df
    ''''''''''''''''''

    def drop_missing_data(self):
        self.playlist_information.dropna(inplace=True)


    def load_all_playlist_info_from_spotify(self, sp):
        print(f"Loading playlist {self.id} information from Spotify...")
        playlist_information = []
        artist_top_track_ids = []

        ''' Songs in playlist '''
        for i in range(0, len(self.playlist_track_ids), 50):
            try:
                tracks_info = sp.tracks(self.playlist_track_ids[i: i + 50])['tracks']
                tracks_features = sp.audio_features(self.playlist_track_ids[i:i + 50])
                for k, track in enumerate(tracks_info):
                    print(i + k)
                    if track:
                        artists = track['artists']
                        artist_ids = []
                        for artist in artists:
                            artist_ids.append(artist['id'])
                        try:
                            artist_info = sp.artists(artist_ids)['artists']
                        except:
                            artist_info = None


                        for artist in artist_ids:
                            try:
                                top_tracks = sp.artist_top_tracks(artist, country='US')['tracks']
                                for top_track in top_tracks:
                                    artist_top_track_ids.append(top_track['id'])
                            except:
                                pass

                        playlist_information.append({
                            'id': track['id'],
                            'track_info': track,
                            'track_features': tracks_features[k],
                            'artists_info': artist_info
                        })
            except:
                pass


        ''' Get the top songs of the artists in the playlist '''
        print(f"Loading top 10 song information for artists in playlist from Spotify...")
        self.artist_top_track_ids = list(set(artist_top_track_ids))
        artist_top_tracks = []
        for i in range(0, len(self.artist_top_track_ids), 50):
            try:
                tracks_info = sp.tracks(self.artist_top_track_ids[i: i + 50])['tracks']
                tracks_features = sp.audio_features(self.artist_top_track_ids[i:i + 50])
                for k, track in enumerate(tracks_info):
                    print(i + k)
                    if track:
                        artists = track['artists']
                        artist_ids = []
                        for artist in artists:
                            artist_ids.append(artist['id'])
                        try:
                            artist_info = sp.artists(artist_ids)['artists']
                        except:
                            artist_info = None

                        artist_top_tracks.append({
                            'id': track['id'],
                            'track_info': track,
                            'track_features': tracks_features[k],
                            'artists_info': artist_info
                        })
            except:
                pass

        self.playlist_information = pd.DataFrame(playlist_information)
        self.artist_top_tracks = pd.DataFrame(artist_top_tracks)
        print(f"Done.")

    def load_artist_to_top_tracks(self, sp):
        """
        Maps artist ids to their top 10 track ids
        """
        print(f"Mapping playlist {self.id} artist ids to their top 10 track ids...")
        artist_ids = []
        for y in self.playlist_information.artists_info.values:
            for x in y:
                artist_ids.append(x['id'])
        artist_ids = list(set(artist_ids))

        self.artist_to_top_tracks = {}
        for i, artist in enumerate(artist_ids):
            print(i)
            try:
                top_tracks = sp.artist_top_tracks(artist, country='US')['tracks']
                top_track_ids = []
                for top_track in top_tracks:
                    top_track_ids.append(top_track['id'])
                self.artist_to_top_tracks[artist] = top_track_ids
            except:
                pass

        print("Done")

    def load_artist_top_tracks_information_into_df(self):
        """
        Fills out a dataframe getting the average feature values for artists' top 10 songs
        """
        artist_top_track_information_df = pd.DataFrame()

        avg_popularity_artist_top_tracks = []
        avg_duration_artist_top_tracks = []
        avg_acousticness_artist_top_tracks = []
        avg_danceability_artist_top_tracks = []
        avg_energy_artist_top_tracks = []
        avg_instrumentalness_artist_top_tracks = []
        avg_liveness_artist_top_tracks = []
        avg_loudness_artist_top_tracks = []
        avg_speechiness_artist_top_tracks = []
        avg_valence_artist_top_tracks = []
        avg_tempo_artist_top_tracks = []

        for artists in self.playlist_information.artists_info.values:
            popularities, durations, acousticnesses, danceabilities, energies, instrumentalnesses, livenesses, loudnesses, speechinesses, valences, tempos = [], [], [], [], [], [], [], [], [], [], []

            for artist_info in artists:
                artist_top_songs = self.artist_top_tracks[
                    self.artist_top_tracks.id.isin(self.artist_to_top_tracks[artist_info['id']])]

                for i in range(artist_top_songs.shape[0]):

                    if artist_top_songs.iloc[i].track_info:
                        popularities.append(artist_top_songs.iloc[i].track_info['popularity'])

                    if artist_top_songs.iloc[i].track_features:
                        artist_top_track_features = artist_top_songs.iloc[i].track_features

                        durations.append(artist_top_track_features['duration_ms'] / 1000)
                        acousticnesses.append(artist_top_track_features['acousticness'])
                        danceabilities.append(artist_top_track_features['danceability'])
                        energies.append(artist_top_track_features['energy'])
                        instrumentalnesses.append(artist_top_track_features['instrumentalness'])
                        livenesses.append(artist_top_track_features['liveness'])
                        loudnesses.append(artist_top_track_features['loudness'])
                        speechinesses.append(artist_top_track_features['speechiness'])
                        valences.append(artist_top_track_features['valence'])
                        tempos.append(artist_top_track_features['tempo'])

            avg_popularity_artist_top_tracks.append(np.array(popularities).mean() if len(popularities) > 0 else None)
            avg_duration_artist_top_tracks.append(np.array(durations).mean() if len(durations) > 0 else None)
            avg_acousticness_artist_top_tracks.append(
                np.array(acousticnesses).mean() if len(acousticnesses) > 0 else None)
            avg_danceability_artist_top_tracks.append(
                np.array(danceabilities).mean() if len(danceabilities) > 0 else None)
            avg_energy_artist_top_tracks.append(np.array(energies).mean() if len(energies) > 0 else None)
            avg_instrumentalness_artist_top_tracks.append(
                np.array(instrumentalnesses).mean() if len(instrumentalnesses) > 0 else None)
            avg_liveness_artist_top_tracks.append(np.array(livenesses).mean() if len(livenesses) > 0 else None)
            avg_loudness_artist_top_tracks.append(np.array(loudnesses).mean() if len(loudnesses) > 0 else None)
            avg_speechiness_artist_top_tracks.append(np.array(speechinesses).mean() if len(speechinesses) > 0 else None)
            avg_valence_artist_top_tracks.append(np.array(valences).mean() if len(valences) > 0 else None)
            avg_tempo_artist_top_tracks.append(np.array(tempos).mean() if len(tempos) > 0 else None)

        artist_top_track_information_df['avg_popularity_artist_top_tracks'] = pd.Series(avg_popularity_artist_top_tracks)
        artist_top_track_information_df['avg_duration_artist_top_tracks'] = pd.Series(avg_duration_artist_top_tracks)
        artist_top_track_information_df['avg_acousticness_artist_top_tracks'] = pd.Series(avg_acousticness_artist_top_tracks)
        artist_top_track_information_df['avg_danceability_artist_top_tracks'] = pd.Series(avg_danceability_artist_top_tracks)
        artist_top_track_information_df['avg_energy_artist_top_tracks'] = pd.Series(avg_energy_artist_top_tracks)
        artist_top_track_information_df['avg_instrumentalness_artist_top_tracks'] = pd.Series(avg_instrumentalness_artist_top_tracks)
        artist_top_track_information_df['avg_liveness_artist_top_tracks'] = pd.Series(avg_liveness_artist_top_tracks)
        artist_top_track_information_df['avg_loudness_artist_top_tracks'] = pd.Series(avg_loudness_artist_top_tracks)
        artist_top_track_information_df['avg_speechiness_artist_top_tracks'] = pd.Series(avg_speechiness_artist_top_tracks)
        artist_top_track_information_df['avg_valence_artist_top_tracks'] = pd.Series(avg_valence_artist_top_tracks)
        artist_top_track_information_df['avg_tempo_artist_top_tracks'] = pd.Series(avg_tempo_artist_top_tracks)

        self.artist_top_track_information_df = artist_top_track_information_df

    def load_artist_one_hot_genres_information_into_df(self):
        """
        Fills out a dataframe with one hot encoded information about the artists' genres
        """
        genres = set()
        for artists in self.playlist_information.artists_info.values:
            for artist in artists:
                for genre in artist["genres"]:
                    genres.add(genre)

        genres = list(genres)
        genres_df = []
        for artists in self.playlist_information.artists_info.values:
            song_genres = {'genre_' + genre: 0 for genre in genres}
            for artist in artists:
                for genre in artist["genres"]:
                    song_genres['genre_' + genre] = 1

            genres_df.append(song_genres)

        self.genres_df = pd.DataFrame(genres_df)
