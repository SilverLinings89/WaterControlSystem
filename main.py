from pymongo import MongoClient
import config

SYSTEM_CONFIG_COLLECTION_NAME = "SYSTEM_CONFIG"

client = MongoClient("mongodb+srv://" + config.DATABASE_USER_NAME + ":" + config.DATABASE_USER_PASSWORD + "@" + config.DATABASE_SERVER_NAME +"/?retryWrites=true&w=majority")

db = client[config.DATABASE_NAME]

list_of_collections = db.list_collection_names()

does_collection_exists = False

for collection in list_of_collections:
    if collection == SYSTEM_CONFIG_COLLECTION_NAME:
        does_collection_exists = True

if not does_collection_exists:
    print("Creating new system config collection")
    db.create_collection(SYSTEM_CONFIG_COLLECTION_NAME)

system_config_collection = db[SYSTEM_CONFIG_COLLECTION_NAME]


