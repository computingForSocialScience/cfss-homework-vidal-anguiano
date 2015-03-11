import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    namespace = name.replace(" ","%20")
    url = 'https://api.spotify.com/v1/search?q=' + namespace + '&type=artist'
    req = requests.get(url)
    artistInfo = req.json()
    artists = artistInfo['artists']['items']
    
    if not artists: #If the artistInfo['artists']['items'] is empty, then it returns the error code
    	searchresultid = "Search does not match an artist name"
    else:
    	searchresultid = artists[0]['id']

    return searchresultid


def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
    returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    req = requests.get(url)
    artistInfo = req.json()

    artist_dict = {}

    artist_dict['followers'] = artistInfo['followers']['total']
    artist_dict['genres'] = artistInfo['genres']
    artist_dict['id'] = artistInfo['id']
    artist_dict['name'] = artistInfo['name']
    artist_dict['popularity'] = artistInfo['popularity']

    return artist_dict





