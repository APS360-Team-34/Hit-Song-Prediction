import json
import pickle
import pandas as pd
import numpy as np
from DataProcessing import normalize_dataframe

def save_track_data(track_data, file=None):
    """
    Saves track_data object into a pickle
    :param file: Name of file to save into (default - track_data_[name])
    :return: Name of file that was saved into
    """
    file = f"track_data_{track_data.name}" if file is None else file
    with open(file, 'wb') as f:
        pickle.dump(track_data, f)

    print(f"Saved track data into file: {file}")
    return file

def load_track_data(file):
    """
    Saves track_data object into a pickle
    :param file: Name of file to load from
    :return: Object that was loaded
    """
    with open(file, 'rb') as f:
        track_data = pickle.load(f)

    print(f"Loaded track data from file: {file}")
    return track_data

class TrackData:
    def __init__(self, tracks, name):
        self.tracks_to_use = tracks
        self.name = name

        self.track_list = []
        self.artists_dict = {} # ID -> Name
        self.df = None

    def populate_artist_data(self, sp):
        """
        Gets the artist ids/names and saves them in class
        :param sp: Spotify connection
        """

        ''' Iterate through tracks (50 at a time) whose artists will be used '''
        for i in range(0, len(self.tracks_to_use), 50):
            tracks_info = sp.tracks(self.tracks_to_use[i: i + 50])['tracks']
            ''' Iterate through the 50 tracks '''
            for k, track in enumerate(tracks_info):
                if track:
                    artists = track['artists']
                    ''' Iterate through artists of track '''
                    for artist in artists:
                        self.artists_dict[artist['id']] = artist['name']


    def populate_artist_songs(self, sp):
        """
        Gets the songs of the artists loaded
        """
        for i, (id, artist) in enumerate(self.artists_dict.items(), 0):
            print(i)
            artist_tracks = sp.search('artist:"' + str(artist) + '"', type='track', limit=50, offset=0)['tracks']
            while artist_tracks['next']:
                for track in artist_tracks['items']:
                    self.track_list.append(track['id'])
                try:
                    artist_tracks = sp.next(artist_tracks)['tracks']
                except:
                    break
        self.track_list = list(set(self.track_list))