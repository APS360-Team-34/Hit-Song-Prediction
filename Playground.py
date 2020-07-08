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


