import fetchArtist as fAr
import fetchAlbums as fAl
import albumtest
import csv
import sys
import networkx as nx
import analyzeNetworks as anN
import artistNetworks as arN
import numpy as np
import requests
import pandas as pd

artistids = []
for x in sys.argv[1:]:
	artistids.append(fAr.fetchArtistId(x))

count = 1
listoffilenm = []

for artist in artistids:
	filenm = "edgelist" + str(count) + ".csv"
	arN.writeEdgeList(artist,2,filenm)
	listoffilenm.append(filenm)
	count += 1

numberoffiles = len(listoffilenm)
subsequentindex = 2
counter2 = 2

if len(listoffilenm) != 1:
	file1 = anN.readEdgeList(listoffilenm[0])
	file2 = anN.readEdgeList(listoffilenm[1])
	combinededgelist = file1.append(file2)
if len(listoffilenm) == 1:
	combinededgelist = anN.readEdgeList(listoffilenm[0])

while counter2 < numberoffiles:
	combinededgelist.append(anN.readEdgeList(listoffilenm[subsequentindex]))
	subsequentindex += 1
	counter2 += 1

combinededgelist.to_csv("combinededgelist.csv", index = False)

combinededgelistdf = anN.readEdgeList("combinededgelist.csv")

network = anN.pandasToNetworkX(combinededgelistdf)

listof30artists = []

while len(listof30artists) != 30:
	artist = anN.randomCentralNode(network)
	listof30artists.append(artist)

listof30albums = []

for artist in listof30artists:
	albums = fAl.fetchAlbumIds(artist)
	if len(albums) == 1:
		listof30albums.append(albums[0])
	if len(albums) != 1:
		random_album = np.random.choice(albums)
		listof30albums.append(random_album)

def fetchTracks(album_id):
	"""Takes album_id and returns list of album's tracks"""
	url = "https://api.spotify.com/v1/albums/" + album_id + "/tracks"
	req = requests.get(url)
	trackdata = req.json()['items']

	listoftracks = []

	for track in trackdata:
		track_id = track['id']
		listoftracks.append(track_id)

	return listoftracks

listof30tracks = []

for album in listof30albums:
	tracks = fetchTracks(album)
	random_track = np.random.choice(tracks)
	listof30tracks.append(random_track)

artist_names = []

for artist_id in listof30artists:
	artist_name = fAr.fetchArtistInfo(artist_id)['name']
	artist_names.append(artist_name)

album_names = []

for album_id in listof30albums:
	album_name = fAl.fetchAlbumInfo(album_id)['album_name']
	album_names.append(album_name)

track_names = []

def fetchTrackName(track_id):
	"""Give track_id to retrieve track name"""
	"""Takes album_id and returns list of album's tracks"""
	url = "https://api.spotify.com/v1/tracks/" + track_id
	req = requests.get(url)
	trackdata = req.json()

	trackname = trackdata['name']

	return trackname

for track_id in listof30tracks:
	track_name = fetchTrackName(track_id)
	track_names.append(track_name)

playlist = []

for x in range(len(listof30artists)):
	info_dict = {"artist_name":artist_names[x],"album_name":album_names[x],"track_names":track_names[x]}
	playlist.append(info_dict)

playlistDF = pd.DataFrame(playlist)

playlistDF.to_csv("playlist.csv", index = False, encoding='utf-8')



