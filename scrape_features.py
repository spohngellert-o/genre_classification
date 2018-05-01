import requests
import os
import time
import spotipy
import spotipy.util as util
import sys

def get_all_songs(artist, genre):
	songs = []
	res = spotify.search(q='artist:' + artist, type='artist')
	artist_id = res['artists']['items'][0]['id']
	# print(artist_id)
	res = spotify.artist_albums(artist_id)
	for item in res['items']:
		album_id = item['id']
		res = spotify.album(album_id)
		for track in res['tracks']['items']:
			res = spotify.track(track['id'])
			duration = res['duration_ms']
			song_name = res['name']
			songs.append({'name': song_name, 'duration': duration, 'genre': genre})

api_id = os.getenv('SpotifyApiID')
api_secret = os.getenv('SpotifyApiSecret')
user_id = os.getenv('SpotifyUserID')
scope = 'user-library-read'
spotify = spotipy.Spotify()
token = util.prompt_for_user_token(user_id,scope,client_id=api_id,client_secret=api_secret,redirect_uri='http://oliverspohngellert.com')
artists_dict = {
	'rock': ['Red Hot Chili Peppers'],
	'country': ['Jason Aldean'],
	'rap': ['Jay Z'],
	'pop': ['Justin Bieber']
}
spotify = spotipy.Spotify(auth=token)
all_songs = []
for genre in artists_dict:
	for artist in artists_dict[genre]:
		all_songs += get_all_songs(artist, genre)


