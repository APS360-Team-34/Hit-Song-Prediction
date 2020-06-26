import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from string import ascii_lowercase

import pandas as pd
import json

client_id = "4c1f5e693ba04424ba05284ea525b427"
client_secret = "57a642672e5f4b0fa9255f38a152b2ad"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_num_of_tracks(year):
    """
    Queries and returns the number of tracks in the given year
    :param year: The year to query
    :return: Number of tracks in the given year
    """
    track_results = sp.search('year:' + str(year), type='track', limit=1, offset=0)
    return track_results['tracks']['total']


def track_count(search_string):
    """
    Gets the number of tracks matching the given query
    :param search_string: Spotify query
    :return: Number of tracks matching the query
    """
    track_results = sp.search(search_string, type='track', limit=1, offset=0)
    return track_results['tracks']['total']


def get_next_search_string(letter_ids, last_was_under=True):
    """
    Gets the next alphabetical string that will be seached
    :param letter_ids: The string that was searched last
    :param last_was_under: Whether the string searched last had < 2000 tracks
    :return: List of letter ids 0-A, 1-B...
        None - if end of strings reached
    """
    # Add new letter to the end (A)
    if not last_was_under:
        letter_ids.append(0)
        return letter_ids

    # Increment
    letter_ids[-1] = letter_ids[-1] + 1
    while (letter_ids[-1] > 25):
        if (len(letter_ids) > 1):
            del letter_ids[-1]
            letter_ids[-1] = letter_ids[-1] + 1
        else:
            return None

    return letter_ids


def construct_search_string(letter_ids):
    """
    Creates a string from a list of letter ids 0-A, 1-B
    :param letter_ids: List of indexes for ascii_lowercase
    :return: String constructed from letter_ids
    """
    if letter_ids is None:
        return None

    search_string = ""
    for id in letter_ids:
        search_string += ascii_lowercase[id]
    return search_string


def save_to_json(dict, file):
    """
    Save an object as a json
    :param dict: Object to save
    :param file: Json file to save into
    :return: File that was saved
    """
    with open(file, 'w') as f:
        json.dump(dict, f, indent=2)
    return file


def load_from_json(file):
    """
    Loads data from json file
    :param file: Name of json file to load from
    :return: Loaded object
    """
    with open(file, 'r') as f:
        return json.load(f)


def get_year_tracks(year):
    """
    Pulls track ids and names for a given year from Spotify into json file
    :param year: Year to pull tracks from
    :return: Name of file that data was saved in
    """
    print(f"Total Tracks in {year}: {get_num_of_tracks(year)}")

    query_format = f"year:{year} track:"

    search_string_letter_ids = [0]

    tracks = {}

    total = 0;

    while (search_string_letter_ids is not None):
        search_string = construct_search_string(search_string_letter_ids)
        count = track_count(query_format + search_string)
        print(f"{search_string} : {count}")
        if count < 2000:
            for i in range(0, count, 50):
                track_results = sp.search(query_format + search_string, type='track', limit=50, offset=i)
                for t in track_results['tracks']['items']:
                    if t['id'] not in tracks:
                        total += 1
                        tracks[t['id']] = {'name': t['name']}

            search_string_letter_ids = get_next_search_string(search_string_letter_ids, last_was_under=True)
        else:
            search_string_letter_ids = get_next_search_string(search_string_letter_ids, last_was_under=False)

    print(f"Tracks Saved In File: {total}")

    file = save_to_json(tracks, f"Tracks{year}.json")
    return file


def get_all_tracks():
    """
    Pulls track ids and names from Spotify into json file
    :param year: Year to pull tracks from
    :return: Name of file that data was saved in
    """
    query_format = f"track:"

    search_string_letter_ids = [0]

    tracks = {}

    total = 0

    while search_string_letter_ids is not None:
        search_string = construct_search_string(search_string_letter_ids)
        count = track_count(query_format + search_string)
        print(f"{search_string} : {count}")
        if count < 2000:
            for i in range(0, count, 50):
                track_results = sp.search(query_format + search_string, type='track', limit=50, offset=i)
                for t in track_results['tracks']['items']:
                    if t['id'] not in tracks:
                        total += 1
                        tracks[t['id']] = {'name': t['name']}

            search_string_letter_ids = get_next_search_string(search_string_letter_ids, last_was_under=True)
        else:
            search_string_letter_ids = get_next_search_string(search_string_letter_ids, last_was_under=False)

    print(f"Tracks Saved In File: {total}")

    file = save_to_json(tracks, f"tracks.json")
    return file


def save_playlist_tracks(playlist):
    """
    Saves track IDs from playlist in a json
    :param playlist: Spotify playlist ID
    :return: Name of file where data was saved
    """
    results = sp.playlist_tracks(playlist)
    playlist_tracks = []

    while results['next']:
        for i in results['items']:
            track = i['track']
            playlist_tracks.append(track['id'])
        results = sp.next(results)

    file = save_to_json(playlist_tracks, f"playlist_{playlist}.json")
    return file


def get_playlist_tracks(playlist):
    """
    Gets tracks in a playlist and saves information into a dataframe (saves as csv)
    :param playlist: Spotify playlist ID
    :return: Name of file where data was saved
    """
    track_ids = [id for id in load_from_json(f"playlist_{playlist}.json") if id is not None]
    tracks = []

    for i in range(0, len(track_ids), 50):
        tracks_info = sp.tracks(track_ids[i: i+50])['tracks']
        for track in tracks_info:
            if track:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'popularity': track['popularity']
                })
    df = pd.DataFrame(tracks)

    file = f"playlist_{playlist}_df.csv"
    df.to_csv(file)

    return file


# save_playlist_tracks("2sRZldX6n9oaII70OoO3zB")
get_playlist_tracks("2sRZldX6n9oaII70OoO3zB")



