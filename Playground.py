from SpotifyConnection import get_spotify_connection
import Playlist as PL
from Playlist import Playlist
from DataProcessing import normalize_dataframe, SpotifyTracksDataset

import TrackData as TD
from TrackData import TrackData


sp = get_spotify_connection()

playlist_id = "2sRZldX6n9oaII70OoO3zB"

''' Load playlist tracks'''
# pl = Playlist(playlist_id)
# pl.load_playlist_tracks(sp)
# pl.save_playlist_tracks()
# PL.save_playlist(pl)

# ''' Load playlist dataframe'''
# pl = PL.load_playlist("playlist_" + playlist_id)
# df = pl.load_playlist_df(sp)
# PL.save_playlist(pl)
# #
# ''' Drop tracks with missing data '''
# pl = PL.load_playlist("playlist_" + playlist_id)
# df = pl.drop_missing_data()
# PL.save_playlist(pl)


# pl = PL.load_playlist("playlist_" + playlist_id)
# print(pl.playlist_df.columns)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_all_playlist_info_from_spotify(sp)
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_artist_to_top_tracks(sp)
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_" + playlist_id)
# pl.load_artist_top_tracks_information_into_df()
# PL.save_playlist(pl)

pl = PL.load_playlist("playlist_" + playlist_id)
pl.load_artist_one_hot_genres_information_into_df()
PL.save_playlist(pl)


print(pl.playlist_information.columns)
print(pl.playlist_information)
print(pl.artist_top_tracks.columns)
print(pl.artist_top_tracks)
print(len(pl.artist_top_track_ids))
print(pl.artist_to_top_tracks)
print(pl.artist_top_track_information_df)
print(pl.genres_df)
