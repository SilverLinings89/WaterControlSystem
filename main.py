from pymongo import MongoClient
import config
import time
from PyP100 import PyP110
import json

SYSTEM_CONFIG_COLLECTION_NAME = "SYSTEM_CONFIG"

with open("setup.json", "r") as json_file:
    json_data = json.load(json_file)

client = MongoClient("mongodb+srv://" + config.DATABASE_USER_NAME + ":" + config.DATABASE_USER_PASSWORD + "@" + config.DATABASE_SERVER_NAME +"/?retryWrites=true&w=majority")

db = client[config.DATABASE_NAME]

def does_collection_exist(name):
    global db
    list_of_collections = db.list_collection_names()
    does_collection_exists = False
    for collection in list_of_collections:
        if collection == name:
            does_collection_exists = True
    return does_collection_exist

def open_or_create_collection(collection_name):
    global db
    collection_exists = does_collection_exist(collection_name)
    if not collection_exists:
        db.create_collection(collection_name)
    return db[collection_name]

system_config_collection = open_or_create_collection(SYSTEM_CONFIG_COLLECTION_NAME)

existing_document = system_config_collection.find_one(query)

if existing_document:
    system_config_collection.update_one({}, {"$set": json_data})
else: 
    collection.insert_one(json_data)


p110 = PyP110.P110("ip goes here", config.TP_USER, config.TP_PASSWORD)

p110.handshake()
p110.login()

ret = p110.getEnergyUsage()
print(ret)



client.close()
