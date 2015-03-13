import pymysql
import json
from pprint import pprint

dbname="facebook"
host="localhost"
user="root"
passwd="V1DaL1T0"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()

def createEdgeTable(file_name):
	
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

	cur.executemany(insertQuery,edgelist)

	db.commit()



def createAttributesTable(json_file):

    json_data = open(json_file)
    data = json.load(json_data)

    friend_attribute_list = []

    for friend in data:       # friend indicates one dictionary
        uid = friend["uid"]
        first_name = friend["first_name"]
        middle_name = friend["middle_name"]
        last_name = friend["last_name"]
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

        tupl = (uid, first_name, middle_name, last_name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website)
        friend_attribute_list.append(tupl)

    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS friend_attributes (id INTEGER PRIMARY KEY AUTO_INCREMENT, uid VARCHAR(128), first_name VARCHAR(128), middle_name VARCHAR(128), last_name VARCHAR(128), pic VARCHAR(255), religion VARCHAR(128), birthday_date VARCHAR(128), sex VARCHAR(64), hometown_location VARCHAR(128), current_location VARCHAR(128), relationship_status VARCHAR(64), significant_other_id VARCHAR(128), political VARCHAR(128), locale VARCHAR(64), profile_url VARCHAR(255), website VARCHAR(255));''')

    insertQuery = '''INSERT INTO friend_attributes (uid, first_name, middle_name, last_name, pic, religion, birthday_date, sex, hometown_location, current_location, relationship_status, significant_other_id, political, locale, profile_url, website) \n
                         VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)'''

    cur.executemany(insertQuery, friend_attribute_list)
    db.commit()


createAttributesTable('friend_attributes2.json')










