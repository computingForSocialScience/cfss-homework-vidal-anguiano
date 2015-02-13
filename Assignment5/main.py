import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumInfo
from albumtest import fetchAlbumIds
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    
    artist_ids_list = []

    for artist in artist_names:
    	artist_id = fetchArtistId(artist)
    	artist_ids_list.append(artist_id)

        artist_dicts_list = []

    	for artist_id in artist_ids_list:
            artist_info = fetchArtistInfo(artist_id)
            artist_dicts_list.append(artist_info)

    	writeArtistsTable(artist_dicts_list)

    	album_ids_list = []

    	for artist in artist_ids_list:
    		album_ids_list += fetchAlbumIds(artist)

    	album_dicts_list = []

    	for album in album_ids_list:
    		album_dicts_list.append(fetchAlbumInfo(album))

    	writeAlbumsTable(album_dicts_list)

    plotBarChart()



    

