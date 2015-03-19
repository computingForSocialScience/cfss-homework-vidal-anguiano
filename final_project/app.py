from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import pymysql
import json
from pprint import pprint
import pandas as pd
import networkx as nx
import unicodedata as uni
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt
import os

#Created this function because some of the names in edgelist were not found in my friend_attributes data
def infriend_attributes(name):
	fullfriendlist = []
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()

	sql = '''select name from friend_attributes;'''

	cur.execute(sql)
	fullfriendfetch = cur.fetchall()
	for friend in fullfriendfetch:
		friendname = friend[0]
		fullfriendlist.append(uni.normalize('NFKD', friendname).encode('ascii','ignore'))
	if name in fullfriendlist:
		return True
	else:
		return False

def visualizegraph(graph):
	nx.draw(graph,with_labels=True,font_size=6)
	f = tempfile.NamedTemporaryFile(
		dir='static/temp',
		suffix='.png',delete=False)
	plt.savefig(f)
	plt.clf()
	fname = f.name
	f.close()
	return fname

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def fetchuid(name):
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()
	cur.execute('''SELECT uid FROM friend_attributes WHERE name=''' + '''"''' + str(name) + '''"''')

	uid = cur.fetchall()

	errorcode = 100
	if uid:
		return uid[0][0]
	else:
		return errorcode


def constructGraph(friendName):

	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	sql = '''select * from edges where uid1=''' + '''"''' + str(friendName) + '''"''' + ''' OR uid2=''' + '''"''' + str(friendName) + '''"'''

	pandasdataframe = pd.io.sql.read_sql(sql,db)

	graph = pandasToNetworkX(pandasdataframe)

	return graph

def pandasToNetworkX(edgeList):
    """Creates a NetworkX Digraph from an edge list in
    a pandas data frame"""

    network = nx.DiGraph()

    for col1,col2 in edgeList.to_records(index=False):
        network.add_edge(col1,col2)

    return network

def createEdgeTable(file_name):
	
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()
	json_data = open(file_name) 
	data = json.load(json_data)

	edgelist = []

	for edge in data:
		uid1 = edge['uid1']
		uid2 = edge['uid2']
		edgelist.append((uid1,uid2))

	insertQuery = '''
	insert into edges
	(uid1,uid2)
	values
	(%s,%s)'''
	
	cur.execute('''CREATE TABLE IF NOT EXISTS edges (uid1 VARCHAR(255), uid2 VARCHAR(255));''')

	cur.executemany(insertQuery,edgelist)

	db.commit()


def createAttributesTable(json_file):
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')
	json_data = open(json_file)
	data = json.load(json_data)

	friend_attribute_list = []

	for friend in data:       # friend indicates one dictionary
		uid = friend["uid"]
		first_name = friend["first_name"]
		middle_name = friend["middle_name"]
		last_name = friend["last_name"]
		name = friend["name"]
		pic = friend["pic"]
		religion = friend["religion"]
		birthday_date = friend["birthday_date"]
		sex = friend["sex"]
		if friend["hometown_location"] == None:
			hometown_location = friend["hometown_location"]
		else:
			hometown_location = friend["hometown_location"]["name"]
		if friend["current_location"] == None:
			current_location = friend["current_location"]
		else:
			current_location = friend["current_location"]["name"]
		relationship_status = friend["relationship_status"]
		significant_other_id = friend["significant_other_id"]
		political = friend["political"]
		locale = friend["locale"]
		profile_url = friend["profile_url"]
		website = friend["website"]

		tupl = (uid, first_name, middle_name, last_name, name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website)
		friend_attribute_list.append(tupl)

	cur = db.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS friend_attributes (id INTEGER PRIMARY KEY AUTO_INCREMENT, uid VARCHAR(255), first_name VARCHAR(128), middle_name VARCHAR(128), last_name VARCHAR(128), name VARCHAR(128), pic VARCHAR(255), religion VARCHAR(128), birthday_date VARCHAR(128), sex VARCHAR(64), hometown_location VARCHAR(128), current_location VARCHAR(128), relationship_status VARCHAR(64), significant_other_id VARCHAR(255), political VARCHAR(128), locale VARCHAR(64), profile_url VARCHAR(255), website VARCHAR(255));''')

	insertQuery = '''INSERT INTO friend_attributes (uid, first_name, middle_name, last_name, name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website) \n
                         VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)'''

	cur.executemany(insertQuery, friend_attribute_list)
	db.commit()


UPLOAD_FOLDER = 'C:/cygwin64/home/Vidal/cfss/cfss-homework-vidal-anguiano/final_project'
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    dbname="facebook"
    host="localhost"
    user="root"
    passwd="V1DaL1T0"
    db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

    cur = db.cursor()
    sql = '''
        select uid, first_name, last_name
        from friend_attributes'''

    cur.execute(sql)

    friend_attributes = cur.fetchall()

    return(render_template('index.html',friend_attributes=friend_attributes))

@app.route('/profile/<userid>')
def make_friend_list(userid):
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()
	sql = '''select first_name, middle_name, last_name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, profile_url, website from friend_attributes where uid=''' + str(userid)
	cur.execute(sql)
	friend_attributes = cur.fetchall()

	bur = db.cursor()#Convert userid into name

	bur.execute('''SELECT first_name, middle_name, last_name FROM friend_attributes WHERE uid=''' + str(userid))
	fullNameTupl = bur.fetchall()
	if fullNameTupl[0][1]: #If middle name exists, assign first, middle, and last to friendName
		friendName = fullNameTupl[0][0] + " " + fullNameTupl[0][1] + " " + fullNameTupl[0][2]
	else:
		friendName = fullNameTupl[0][0] + " " + fullNameTupl[0][2]

	friendName1 = uni.normalize('NFKD', friendName).encode('ascii','ignore')

	g = constructGraph(friendName1)
	friendList = g.nodes()

	friendList1 = []
	

	#This loop changes unicode names to acsii
	for named in friendList:
		friendList1.append(uni.normalize('NFKD', named).encode('ascii','ignore'))


	uidList = []
	for named in friendList1:
		uid = fetchuid(named)
		uidList.append(uid)

	uidNameList = zip(uidList, friendList1)

	#Variable for counting mutual friends. I subtract 1 for user's own name.
	friendscommon = len(friendList1) - 1
	# Create png file 
	fname = visualizegraph(g)
	plotPng = "/static/temp/" + str(os.path.split(fname)[-1])

	return(render_template('profile.html',friendscommon=friendscommon,friend_attributes=friend_attributes,uidNameList=uidNameList,plotPng=plotPng))


@app.route('/upload', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		fileatr = request.files['attributes']
		if fileatr and allowed_file(fileatr.filename):
			filename = secure_filename(fileatr.filename)
			fileatr.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		fileedge = request.files['edges']
		if fileedge and allowed_file(fileedge.filename):
			filename = secure_filename(fileedge.filename)
			fileedge.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return render_template('upload.html')

@app.route('/100')
def error_page():
	return render_template('error.html')

@app.route('/createtables')
def createtables():
	dbname="facebook"
	host="localhost"
	user="root"
	passwd="V1DaL1T0"
	db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

	cur = db.cursor()
	sql = '''drop table if exists edges,friend_attributes;'''
	cur.execute(sql)
	createAttributesTable('attributes.json')
	createEdgeTable('edges.json')
	return render_template('tablescreated.html')

if __name__ == '__main__':
	app.debug=True
	app.run()
