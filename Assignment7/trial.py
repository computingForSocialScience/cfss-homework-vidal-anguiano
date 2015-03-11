import pymysql
from artistNetworks import *
from analyzeNetworks import *
from fetchAlbums import *
from fetchArtist import *
from pandas import *


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

def fetchTrackName(track_id):
	"""Give track_id to retrieve track name"""
	"""Takes album_id and returns list of album's tracks"""
	url = "https://api.spotify.com/v1/tracks/" + track_id
	req = requests.get(url)
	trackdata = req.json()

	trackname = trackdata['name']

	return trackname

def createNewPlaylist(artistname):
	randomartists = []
	randomalbums = []
	randomalbumss = []
	randomtracks = []

	artistid = fetchArtistId(artistname)
	edgelist = getEdgeList(artistid,2)
	net = pandasToNetworkX(edgelist)

	while len(randomartists) < 30:
		random = randomCentralNode(net)
		randomartists.append(random)

	singleslist = []

	for artist in randomartists:
		albums = fetchAlbumIds(artist)
		if len(albums) == 0:
			url = "https://api.spotify.com/v1/artists/" + artist + "/albums?&album_type=single"
			req = requests.get(url)
			singledata = req.json()['items']
			for	x in singledata:
				singleslist.append(x['id'])
			randomalbums.append(np.random.choice(singleslist))
		else:
			randomalbums.append(np.random.choice(albums))

	for album in randomalbums:
		tracks = fetchTracks(album)
		randomtracks.append(np.random.choice(tracks))

	artist_names = []

	for artist_id in randomartists:
		artist_names.append(fetchArtistInfo(artist_id)['name'])

	album_names = []

	for album_id in randomalbums:
		album_names.append(fetchAlbumInfo(album_id)['album_name'])

	track_names = []	

	for track_id in randomtracks:
		track_names.append(fetchTrackName(track_id))

	dbname="playlists"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()

	cur.execute('''
		create table if not exists playlists (
		id integer primary key
		auto_increment,
		rootArtist varchar(255));''')

	cur.execute('''
		create table if not exists songs (
		playlistId integer,
		songOrder integer,
		artistName varchar(255),
		albumName varchar(255),
		trackName varchar(255));''')

	playlist = []
	
	cur.execute('''
	select * from playlists;''')

	playlistId = cur.fetchall()

	if playlistId:
		playlist_Id = playlistId[-1][0]
		playlist_Id = playlist_Id + 1
	else:
		playlist_Id = 1

	songOrder = range(1,31)

	for x in range(len(artist_names)):
		playlist.append((playlist_Id,songOrder[x],artist_names[x],album_names[x],track_names[x]))


	artist_name = artistname

	cur.execute('''
		insert into playlists
		(rootArtist)
		values
		(%s)''', artist_name)

	db.commit()

	insertQuery = '''
	insert into songs
	(playlistId,songOrder,artistName,albumName,trackName)
	values
	(%s,%s,%s,%s,%s)'''

	cur.executemany(insertQuery,playlist)

	db.commit()

createNewPlaylist("Prince Royce")

