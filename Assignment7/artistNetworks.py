import requests
import pandas as pd
import unicodedata

def getRelatedArtists(artistID):
    """This function takes an artist ID as its only
    argument and returns a list of related artists IDs"""
    url = 'https://api.spotify.com/v1/artists/' + artistID + '/related-artists'
    req = requests.get(url)
    artistData = req.json()['artists']

    relatedartistIDs = []

    for x in artistData:
        artistID = x['id']
        artistIDasc = artistID.encode("ascii")
        relatedartistIDs.append(artistIDasc)
        
    return relatedartistIDs


def getDepthEdges(artistID, depth):
    """Takes two arguments, an artist ID and an integer `depth` and 
    returns a list of tuples representing the directed pairs of 
    related artists"""
    
    initialartistlist = getRelatedArtists(artistID)
    edgelist = []
    counter = 1
    
    for artist in initialartistlist:
        edgelist.append((artistID, artist))
        
    subsequentartistlist = []
    templist = []
    
    while counter < depth:
        for artist in initialartistlist:
            subsequentartistlist = getRelatedArtists(artist)
            for tartist in subsequentartistlist:
                edgelist.append((artist,tartist))
                templist.append(tartist)
        counter += 1
        subsequentartistlist = templist
        templist = []
        
    return edgelist



def getEdgeList(artistID, depth):
    """takes arguments artistID and depth and 
    returns the result as a Pandas DataFrame 
    with one row for each edge"""

    listoftuples = getDepthEdges(artistID, depth)
    listofdicts = []
    rowdict = {}

    for x in listoftuples:
        listofdicts.append({'artist1':x[0],'artist2':x[1]})

    edgelist_df = pd.DataFrame(listofdicts)

    return edgelist_df


        
def writeEdgeList(artistID, depth, filename):
    """generates an edge list based on artstID and depth and 
    writes that to a CSV file specified by the filename 
    parameter"""

    dataframe = getEdgeList(artistID, depth)
    csvfile = dataframe.to_csv(filename, index = False)


