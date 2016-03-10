#this is a reference File
#To use this file fill the following authentication variables and
#remove the '_Example' from file name, it is necessary to use this tool and get

from pymongo import MongoClient

user = 'your_mongodb_user'
password = 'your_mongodb_password*'
serverUrl = 'your_server_name_or_ip'
port = '27017'  #Default 27017
database = 'your_mongodb_database'
collection = 'your_mongodb_collection'   #Where those tweets are stored
uri = 'mongodb://%s:%s@%s:%s' % (user, password, serverUrl,port)
client = MongoClient(uri)
db = client[database]
coll = db[collection]

def getDB():
    return db

def getClient():
    return client

def gedCollection():
    return coll

if __name__ == "__main__":
    print("Your MongoDB Config Values are here")
    print uri
    print db


