import pdb
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyOAuth

scope = [
    "playlist-read-collaborative",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
    "user-read-email",
    "user-read-private",
    "user-library-modify",
    "user-library-read",
    "user-top-read"
]


username="bzone71"
client_id='fab74be9949747e0a66b558f3c92f438'
client_secret = None
redirect_uri='http://127.0.0.1:9090'


with open("client_secret.txt") as secret_fin:
    client_secret = secret_fin.read()

def get_sp():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri))

def get_all_saved_tracks(sp):

    results = sp.current_user_saved_tracks()
    all_items = results['items']
    while results:
        results = sp.next(results)
        if results:
            all_items.extend(results['items'])

    return all_items

def track_list_to_name_list(track_list):
    return [track['track']['name'] for track in track_list]

def get_owned_playlists(sp):
    results = sp.current_user_playlists()
    all_items = results['items']
    while results:
        results = sp.next(results)
        if results:
            all_items.extend(results['items'])

    return [item for item in all_items if item['owner']['id'] == username]

def get_playlist_danceability(sp, playlist_name):
    op = get_owned_playlists(sp)
    swing = [playlist for playlist in op if playlist['name'] == playlist_name][0]

    swing_items = sp.playlist_items(swing['id'])['items']
    for item in swing_items:
        features = sp.audio_features(item['track']['id'])
        print(f"{item['track']['name']}: {features[0]['danceability']}")



# results = sp.current_user_saved_tracks()

# for idx, item in enumerate(results['items']):
#     if idx == 0:
#         print(idx)
#         pprint(item)
