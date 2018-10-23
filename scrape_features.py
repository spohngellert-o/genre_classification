import requests
import os
import time
import spotipy
import spotipy.util as util
from bs4 import BeautifulSoup
import pandas as pd


def request_song_info(song_title, artist_name):
	# print("here")
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + discord_token}
	search_url = base_url + '/search'
	data = {'q': song_title + ' ' + artist_name}
	response = requests.get(search_url, data=data, headers=headers)
	json = response.json()
	remote_song_info = None
	# print(json['response']['hits'][0]['result']['primary_artist']['name'])
	# sys.exit(0)
	for hit in json['response']['hits']:
		# print("{}: {}".format(hit['result']['full_title'], hit['result']['primary_artist']['name'].lower()))
		if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
			remote_song_info = hit
			break
	if remote_song_info:
		song_url = remote_song_info['result']['url']
		page = requests.get(song_url)
		html = BeautifulSoup(page.text, 'html.parser')
		lyrics = html.find('div', class_='lyrics').get_text()
		return lyrics
	else:
		return None



def get_all_songs(artist, genre):
	print("------ STARTING ARTIST {} -------".format(artist))
	songs = []
	try:
		
		res = spotify.search(q='artist:' + artist, type='artist')
		artist_id = res['artists']['items'][0]['id']
		# print(artist_id)
		collected_songs = []
		res = spotify.artist_albums(artist_id)
		for item in res['items']:
			album_id = item['id']
			res = spotify.album(album_id)
			for track in res['tracks']['items']:
				if len(songs) >= 50:
					return songs
				res = spotify.track(track['id'])
				duration = res['duration_ms']
				song_name = res['name']
				if song_name.lower() in collected_songs:
					continue
				lyrics = request_song_info(song_name, artist)
				if lyrics != None:
					collected_songs.append(song_name.lower())
					# print("YAY ------------------------------------")
					print("Got {}".format(song_name))
					# print("Lyrics: {}".format(lyrics[0:100]))
					songs.append({'name': song_name, 'duration': duration, 'genre': genre, 'lyrics': lyrics})
		return songs

	except:
		return songs
api_id = os.getenv('SpotifyApiID')
api_secret = os.getenv('SpotifyApiSecret')
user_id = os.getenv('SpotifyUserID')
discord_token = os.getenv('DISCORD_TOKEN')
scope = 'user-library-read'
spotify = spotipy.Spotify()
token = util.prompt_for_user_token(user_id,scope,client_id=api_id,client_secret=api_secret,redirect_uri='http://oliverspohngellert.com')
artists_dict = {
	'rap': ['Jay-Z', 'Kanye West', 'J. Cole', 'Kendrick Lamar'],
	'rock': ['Red Hot Chili Peppers', 'The Beatles', 'The Rolling Stones'],
	'country': ['Jason Aldean'],
	'pop': ['Justin Bieber', 'Taylor Swift', 'Ariana Grande']
}
spotify = spotipy.Spotify(auth=token)
all_songs = []
for genre in artists_dict:
	for artist in artists_dict[genre]:
		songs = get_all_songs(artist, genre)
		if songs != None:
			 all_songs += songs
			 print(len(all_songs))

		data = pd.DataFrame(all_songs)
		data.to_csv("lyrics.csv", index=False)
		time.sleep(30)

			 # sys.exit(0)

data = pd.DataFrame(all_songs)

data.to_csv("lyrics.csv", index=False)
