from SpotifyConnection import get_spotify_connection
import Playlist as PL
from Playlist import Playlist
from DataProcessing import normalize_dataframe, DataInformation, SpotifyTracksDataset


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data.sampler import SubsetRandomSampler

sp = get_spotify_connection()

# pl = Playlist("2sRZldX6n9oaII70OoO3zB")
# pl.load_playlist_tracks(sp)
# PL.save_playlist(pl)

# pl = PL.load_playlist("playlist_2sRZldX6n9oaII70OoO3zB")
# df = pl.load_playlist_df(sp)
# PL.save_playlist(pl)

pl = PL.load_playlist("playlist_2sRZldX6n9oaII70OoO3zB")
df = pl.get_playlist_df(cols=DataInformation.list())
normalized_df = normalize_dataframe(df)



class TestNet(nn.Module):
    def __init__(self):
        super(TestNet, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(13, 50),
            nn.Sigmoid(),
            nn.Linear(50,1),
            nn.Sigmoid()
        )
    def forward(self, x):
        x = self.layers(x)
        return x

lr = 0.01
bs = 50

net = TestNet()
criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=lr)

ds = SpotifyTracksDataset(normalized_df)
train_loader = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)

num_epochs = 25
for epoch in range(num_epochs):
    print(epoch)
    error = 0
    for features, targets in train_loader:
        optimizer.zero_grad()

        out = net(features)
        loss = criterion(out, targets)
        loss.backward()
        optimizer.step()

        error += (targets - out).abs().sum().item()

    print(error / len(ds))
