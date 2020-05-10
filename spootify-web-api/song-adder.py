import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def parse_tracks():
    # parse track names from songs text file
    track_list = open('songs.txt').read().splitlines()
    get_track_ids(track_list)

def get_track_ids(track_list):
    track_id_list = []

    # Don't forget to set env. variables SPOTIPY_CLIENT_ID= and SPOTIPY_CLIENT_SECRET= (export command) SPOTIPY_REDIRECT_URI=http://localhost/
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # iterate through track list and search spotify web API for track ID to build ID list
    for track in track_list:
        by_start = re.search('by',track).start()
        results = sp.search(q=track[0:(by_start-1)], type='track', limit=1)
        items = results['tracks']['items']
        try:
            track_id = items[0]['id']
        except:
            print('track id not found for ' + track)
        track_id_list.append(track_id)

    add_to_playlist(track_id_list)

# for debugging
# for id in track_id_list: print(id)

def add_to_playlist(track_id_list):
    # username and playlist ID 
    username = ''
    playlist_id = ''

    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_id_list)
        print(results)
    else:
        print("Can't get token for", username)

# Main method
if __name__ == '__main__':
    parse_tracks()



    
