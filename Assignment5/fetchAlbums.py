import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    data = req.json()
    list_of_album_ids = []
    for album in data['items']:
       list_of_album_ids.append(album['id'])

    return list_of_album_ids


def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    album = req.json()

    albuminfo = {}

    albuminfo['artist_id'] = album['artists'][0]['id']
    albuminfo['artist_name'] = album['artists'][0]['name']
    albuminfo['album_id'] = album['id']
    albuminfo['album_name'] = album['name']
    albuminfo['release_year'] = album['release_date'][0:4]
    albuminfo['popularity'] = album['popularity']

    return albuminfo