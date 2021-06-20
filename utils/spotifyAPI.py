import spotipy
from config.config import *

scope = 'user-read-currently-playing'
token = spotipy.util.prompt_for_user_token(USERNAME, scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, cache_path=r"./config/.cache-" + USERNAME)

def get_curr_song(token):
    inst = spotipy.Spotify(auth=token)
    current_song = inst.currently_playing()
    return current_song

def get_artist(songobj):
    artist = songobj['item']['artists'][0]['name']
    return artist

def get_song_name(songobj):
    name = songobj['item']['name']
    return name

def song_info():
    song = get_curr_song(token)
    artist = get_artist(song)
    name = get_song_name(song)
    return artist, name