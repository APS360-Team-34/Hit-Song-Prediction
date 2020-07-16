from SpotifyConnection import get_spotify_connection
import Playlist as PL
from Playlist import Playlist
from DataProcessing import normalize_dataframe, SpotifyTracksDataset

import TrackData as TD
from TrackData import TrackData


def get_track_ids_by_artist(artist_name, artist_id):
    query = f'artist:"{artist_name}"'
    search_result = sp.search(query, type='track', limit=50, offset=0)['tracks']
    artist_tracks = []
    while search_result['next']:
        for track in search_result['items']:
            by_artist = False
            for artist in track['artists']:
                if artist['id'] == artist_id:
                    by_artist = True
            if track['id']:
                if by_artist:
                    artist_tracks.append(track['id'])
        search_result = sp.next(search_result)['tracks']

    for track in search_result['items']:
        if track['id']:
            artist_tracks.append(track['id'])
    return artist_tracks

sp = get_spotify_connection()

playlist_id = "4wVOVUOLCGhkwcehwpju6V"

''' Load playlist tracks'''
# pl = Playlist(playlist_id)
# pl.load_playlist_tracks(sp)
# pl.save_playlist_tracks()
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_all_playlist_info_from_spotify(sp)
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_artist_to_top_tracks(sp)
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_artist_top_tracks_information_into_df()
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_artist_one_hot_genres_information_into_df()
# PL.save_playlist(pl)

pl = PL.load_playlist("playlist_" + playlist_id)
pl.drop_missing_data()
PL.save_playlist(pl)



# print(pl.playlist_information.columns)
# print(pl.playlist_information)
# print(pl.artist_top_tracks.columns)
# print(pl.artist_top_tracks)
# print(len(pl.artist_top_track_ids))
# print(pl.artist_to_top_tracks)
# print(pl.artist_top_track_information_df)
# print(pl.genres_df)


''' ED SHEERAN '''
# artist_name = "Ed Sheeran"
# artist_id = "6eUKZXaKkcviH0Ku9w2n3V"
# playlist_id = "EdSheeran"
# ed_tracks = get_track_ids_by_artist(artist_name, artist_id)
# ed_sheeran_playlist = Playlist(playlist_id)
# ed_sheeran_playlist.playlist_track_ids = ed_tracks
# PL.save_playlist(ed_sheeran_playlist)

# ed_sheeran_playlist = PL.load_playlist("playlist_" + playlist_id)
# ed_sheeran_playlist.load_all_playlist_info_from_spotify(sp)
# PL.save_playlist(ed_sheeran_playlist)

# ed_sheeran_playlist = PL.load_playlist("playlist_" + playlist_id)
# ed_sheeran_playlist.load_artist_to_top_tracks(sp)
# PL.save_playlist(ed_sheeran_playlist)

# ed_sheeran_playlist = PL.load_playlist("playlist_" + playlist_id)
# ed_sheeran_playlist.load_artist_top_tracks_information_into_df()
# PL.save_playlist(ed_sheeran_playlist)

# ed_sheeran_playlist = PL.load_playlist("playlist_" + playlist_id)
# ed_sheeran_playlist.load_artist_one_hot_genres_information_into_df()
# PL.save_playlist(ed_sheeran_playlist)

# print(len(ed_sheeran_playlist.playlist_track_ids))
# print(len(ed_tracks))
