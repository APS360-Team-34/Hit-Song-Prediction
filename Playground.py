from SpotifyConnection import get_spotify_connection
import Playlist as PL
from Playlist import Playlist
from DataProcessing import normalize_dataframe, DataInformation, SpotifyTracksDataset

import TrackData as TD
from TrackData import TrackData


sp = get_spotify_connection()

''' Load playlist tracks'''
# pl = Playlist("2sRZldX6n9oaII70OoO3zB")
# pl.load_playlist_tracks(sp)
# pl.save_playlist_tracks()
# PL.save_playlist(pl)

''' Load playlist dataframe'''
# pl = PL.load_playlist("playlist_2sRZldX6n9oaII70OoO3zB")
# df = pl.load_playlist_df(sp)
# PL.save_playlist(pl)

''' Drop tracks with missing data '''
# pl = PL.load_playlist("playlist_2sRZldX6n9oaII70OoO3zB")
# df = pl.drop_missing_data()
# PL.save_playlist(pl)




# pl = PL.load_playlist("playlist_6KOwiWg5zwrt83nEcx7HyI")
# df = pl.get_playlist_df(cols=DataInformation.list())
# normalized_df = normalize_dataframe(df)

# trackData = TrackData(pl.get_playlist_tracks(), name="Every_Billboard_Year-End_Top_10_Hit_1951_Present")
# trackData.populate_artist_data(sp)
# TD.save_track_data(trackData)

# trackData = TD.load_track_data("track_data_Every_Billboard_Year-End_Top_10_Hit_1951_Present")
# trackData.populate_artist_songs(sp)
# TD.save_track_data(trackData)

# print(len(trackData.track_list))








