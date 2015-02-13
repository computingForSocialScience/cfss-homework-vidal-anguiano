from io import open

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    writer = open('artists.csv','w',encoding='utf-8')

    writer.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for artist in artist_info_list:
        artistlist = artist_info_list[artist]
        artistname = artistlist['name']
        artistid = artistlist['id']
        followers = artistlist['followers']
        popularity = artistlist['popularity']
        writer.write("%s,\"%s\",%d,%d\n" % (artistid,artistname,followers,popularity))


    writer.close()


def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    writer = open('albums.csv','w',encoding='utf-8')

    writer.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    for x in range(len(album_info_list)):
        albumlist = album_info_list[x]
        artistname = albumlist['artist_name']
        artistid = albumlist['artist_id']
        albumid = albumlist['album_id']
        albumname = albumlist['album_name']
        albumyear = int(albumlist['release_year'])
        albumpopularity = albumlist['popularity']

        writer.write('%s,%s,"%s",%d,%d\n' % (artistid,albumid,albumname,albumyear,albumpopularity))


    writer.close()

