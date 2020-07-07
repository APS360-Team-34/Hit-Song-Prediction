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
        ARTIST_POPULARITY = 'artist_popularity'

        @staticmethod
        def list():
            return list(map(lambda f: f.value, DataInformation.Feature))

    """ The target for the model to predict """
    TARGET = 'popularity'

    @staticmethod
    def list():
        return DataInformation.Feature.list() + [DataInformation.TARGET]


    class NormalizationType(Enum):
        """
        Types of normalization that can be performed
        """
        DEFAULT = 0
        STD_CLAMP = 1

    normalization = {
        Feature.DURATION : NormalizationType.STD_CLAMP
    }






class SpotifyTracksDataset(Dataset):
    """
    Dataset of Spotify Songs and their features
    """
    def __init__(self, df, features, target):
        self.df = df
        self.features = features
        self.target = target

    def __getitem__(self, index):
        if isinstance(index, slice):
            all_features = torch.FloatTensor()
            all_labels = torch.FloatTensor()
            for i in range(slice.start, slice.stop, slice.step):
                features = torch.FloatTensor(self.df[self.features].iloc[index])
                label = torch.FloatTensor(np.asarray([self.df[self.target].iloc[index]]))
                all_features = torch.cat(all_features, features, dim=1)
                all_labels = torch.cat(all_labels, label, dim=1)

            return all_features, all_labels
        else:
            features = torch.FloatTensor(self.df[self.features].iloc[index])
            label = torch.FloatTensor(np.asarray([self.df[self.target].iloc[index]]))
            return features, label

    def __len__(self):
        return self.df.shape[0]

    def getitem(self, index):
        return self.df[self.features].iloc[index]



def normalize_data(data, data_min=None, data_max=None):
    """
    Normalize the data
    :param data: Data to normalize
    :param data_min: The minimum possible value of data
    :param data_max: The maximum possible value of data
    :return: Normalized data
    """
    if data_min is None:
        data_min = data.min()
    if data_max is None:
        data_max = data.max()
    return (data - data_min) / (data_max - data_min)

def normalize_data_by_type(data, normalization_type):
    """
    Normalize the data using the given type of normalization
    :param data: The data to normalize
    :param normalization_type: The type of normalization to use (DataInformation.NormalizationType)
    :return: Normalized data
    """
    if normalization_type == DataInformation.NormalizationType.STD_CLAMP:
        min_data = data.mean() - data.std()
        max_data = data.mean() + data.std()
        data = data.clip(lower=min_data, upper=max_data)
    else:
        min_data = data.min()
        max_data = data.max()

    return normalize_data(data, data_min=min_data, data_max=max_data)

def normalize_dataframe(df, cols_to_normalize):
    """
    Nomalize the columns of a dataframe
    :param df: Dataframe to normalize
    :return: Normalized dataframe
    """
    normalized_df = df.copy()
    for col in cols_to_normalize:
        min_value = df[col].min()
        max_value = df[col].max()
        normalized_df[col] = (df[col] - min_value) / (max_value - min_value)
    return normalized_df
