from enum import Enum
from torch.utils.data import Dataset, DataLoader
import torch
import numpy as np


class DataInformation:
    """
    Holds information about the data being used
    """

    class Feature(Enum):
        """
        Track features being used in prediction
        """
        DURATION = 'duration'
        KEY = 'key'
        MODE = 'mode'
        TIME_SIGNATURE = 'time_signature'
        ACOUSTICNESS = 'acousticness'
        DANCEABILITY = 'danceability'
        ENERGY = 'energy'
        INSTRUMENTALNESS = 'instrumentalness'
        LIVENESS = 'liveness'
        LOUDNESS = 'loudness'
        SPEECHINESS = 'speechiness'
        VALENCE = 'valence'
        TEMPO = 'tempo'

        @staticmethod
        def list():
            return list(map(lambda f: f.value, DataInformation.Feature))

    """ The target for the model to predict """
    TARGET = 'popularity'

    @staticmethod
    def list():
        return DataInformation.Feature.list() + [DataInformation.TARGET]


class SpotifyTracksDataset(Dataset):
    """
    Dataset of Spotify Songs and their features
    """
    def __init__(self, df):
        self.df = df
        self.features = DataInformation.Feature.list()
        self.target = DataInformation.TARGET

    def __getitem__(self, index):
        features = torch.FloatTensor(self.df[self.features].iloc[index])
        label = torch.FloatTensor(np.asarray([self.df[self.target].iloc[index]]))
        return features, label

    def __len__(self):
        return self.df.shape[0]

    def getitem(self, index):
        return self.df[self.features].iloc[index]


def normalize_dataframe(df):
    """
    Nomalize the columns of a dataframe
    :param df: Dataframe to normalize
    :return: Normalized dataframe
    """
    normalized_df = df.copy()
    for col in df.columns:
        min_value = df[col].min()
        max_value = df[col].max()
        normalized_df[col] = (df[col] - min_value) / (max_value - min_value)
    return normalized_df