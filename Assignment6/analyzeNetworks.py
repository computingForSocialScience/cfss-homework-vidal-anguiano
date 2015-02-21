import pandas as pd
import networkx as nx

def readEdgeList(filename):
    """reads an edgelist from a CSV with the filename, 
    and returns a Pandas DataFrame with one row for each edge"""

    readcsvfile = pd.read_csv(filename)

    if len(readcsvfile.columns) > 2:
        print "WARNING: This CSV contains more than 2 columns!"
        return pd.read_csv(filename, usecols=[0,1])
    else:
        
        return readcsvfile


def degree(edgeList, in_or_out):
    """Counts the degree of a node. Specify in argument whether in or out degrees
    are to be counted."""

    df = readEdgeList(edgeList)

    if in_or_out == "in":
        count = df['artist2'].value_counts()
        return count
    if in_or_out == "out":
        count = df['artist1'].value_counts()
        return count


def combineEdgeLists(edgeList1, edgeList2):
    """combines two edgeLists, dropping duplicates"""
    
    edgelist1 = readEdgeList(edgeList1)
    edgelist2 = readEdgeList(edgeList2)
    
    combinedlist = edgelist1.append(edgelist2)
    dupremoved = combinedlist.drop_duplicates()

    return dupremoved

def pandasToNetworkX(edgeList):
	"""Creates a NetworkX Digraph from an edge list in
	a pandas data frame"""

	edgelist = readEdgeList(edgeList)

	edgelist.to_records()




