import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv') #defining variable `f_artists` as the 'artists.csv'
    f_albums = open('albums.csv') #defining variable `f_albums` as the 'albums.csv'

    artists_rows = csv.reader(f_artists) 
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    artist_names = [] #Empty list created for use below
    
    decades = range(1900,2020, 10) #creates a list of numbers from 1900 to 2010 by increments of 10
    decade_dict = {} #create empty dictionary
    for decade in decades: #Loops through all of the "1900", "1910", "1920", etc.
        decade_dict[decade] = 0 #In the empty dictionary defined above, each of these values ("1900", "1910", etc.) becomes a key with the value for each of these keys becoming 0

    for artist_row in artists_rows: #loops over each row in the csv file of artists
        if not artist_row: #If there is a blank row, the loop skips it going to the next one
            continue
        artist_id, name, followers, popularity = artist_row
        artist_names.append(name) #adds the name of the artist(s) to the empty list created above

    for album_row  in albums_rows: #loops over each row in the csv file of albums
        if not album_row: # if the row is empty, just skip
            continue
        artist_id, album_id, album_name, year, popularity = album_row 
        for decade in decades:  #loops over each decade in the decades list
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)): #if the year in a given row falls between decade "a" and decade "a" + 10... (next line comment)
                decade_dict[decade] += 1 #then a "count" is added for that decade which effectively tallies the number of albums from any given decade
                break   #break after all rows have been iterated through

    x_values = decades #list of decades
    y_values = [decade_dict[d] for d in decades] #list of tallies for albums according to each decade interval in the decades list
    return x_values, y_values, artist_names #return the three lists created in this function

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()  #takes the three lists from before and names sets the varialbes x_vals (x_values list, decades), y_vals (y_values list, talies), artist_names (artist_names list)
    
    fig , ax = plt.subplots(1,1) 
    ax.bar(x_vals, y_vals, width=10) #bars with x_vals on x axis, with y_vals height, and 10 unit width
    ax.set_xlabel('decades') #x axis label is 'decades'
    ax.set_ylabel('number of albums') #y axis label is 'number of albums'
    ax.set_title('Totals for ' + ', '.join(artist_names)) # Title becomes 'Total for "artist name"' with artist name taken from the artist_names list
    plt.show() #shows the bar plot


    
