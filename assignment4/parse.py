import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below
permitshp = readCSV("permits_hydepark.csv")

def get_avg_latlng(permdata):
	'''shows avg lat and lng of construction permits in HP'''
	listhpp = readCSV("permits_hydepark.csv")
	sumlat = 0
	sumlng = 0
	for var in permdata:
		sumlat += float(var[128])
		sumlng += float(var[129])
		avglat = sumlat/len(listhpp)
		avglng = sumlng/len(listhpp)
	return avglng, avglat

print get_avg_latlng(permitshp)



import numpy as np
import matplotlib.pyplot as plt

def zip_code_barchart(data):
	listhpp = readCVS("permits_hydepark.csv")
	zipcodes = ()
	for lis in listhpp: 
		zipcoder = [line[28], line[35], line[42], line[49], line[56], line[63], line[70], line[77], line[84], line[91], line[98]]
		for zipp in zipcpder:
			if zipp == "": continue	
			zipp = zipp.split("-") 
			zipp = zipp[0]
			if zipp not in contractorZip:
				contractorZip[zipp] = 1
			else: contractorZip[zipp] += 1

	plt.bar(range(len(contractorZip)), contractorZip.values(), align='center')
	plt.xticks(range(len(contractorZip)), contractorZip.keys(), rotation=25)

	plt.savefig('zipcodebar.jpg')



if sys.argv[1] == "latlong":
	print get_avg_latlng()
elif sys.argv[1] == "hist":
	zip_code_barchart()
else: print "Error; only'latlong' or 'hist' are acceptable"