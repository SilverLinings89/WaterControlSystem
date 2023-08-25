from pymongo import MongoClient
import config
import time
from PyP100 import PyP110
import json
import datetime 

SYSTEM_CONFIG_COLLECTION_NAME = "SYSTEM_CONFIG"

client = MongoClient("mongodb+srv://" + config.DATABASE_USER_NAME + ":" + config.DATABASE_USER_PASSWORD + "@" + config.DATABASE_SERVER_NAME +"/?retryWrites=true&w=majority")
db = client[config.DATABASE_NAME]
setup = load_setup()

def load_setup():
    with open("setup.json", "r") as json_file:
        json_data = json.load(json_file)
    return json_data

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

def open_or_create_timeseries_collection(collection_name, granularity): 
    global db
    collection_exists = does_collection_exist(collection_name)
    if not collection_exists:
        db.create_collection(collection_name, timeseries= {
            timeField: "timestamp",
            metaField: "metadata",
            granularity: "seconds"
        })
    return db[collection_name]

def publish_local_setup():
    global setup
    system_config_collection = open_or_create_collection(SYSTEM_CONFIG_COLLECTION_NAME)
    existing_document = system_config_collection.find_one(query)
    if existing_document:
        system_config_collection.update_one({}, {"$set": setup})
    else: 
        collection.insert_one(setup)

def get_ip_from_electriciy_device_name(device_name):
    global setup
    for sensor in setup["power"]:
        if sensor["name"] == device_name:
            return sensor["ip"]
    return ""


def get_data_from_p110(device_name):
    device_ip = get_ip_from_electriciy_device_name(device_name)
    p110 = PyP110.P110(device_ip, config.TP_USER, config.TP_PASSWORD)
    p110.handshake()
    p110.login()
    energy_usage_data = p110.getEnergyUsage()
    return energy_usage_data

def open_or_create_energy_collection(device_name):
    global db
    global setup
    return open_or_create_timeseries_collection("power" + device_name)

def publish_electricity_data(device_name):
    electricity_collection = open_or_create_energy_collection(device_name)
    measurement = get_data_from_p110(device_name)
    time_series_entry = {
        "timestamp": datetime.datetime.now(),
        "metadata": {
            "uptime_today(min)": measurement['result']['today_runtime'],
            "uptime_month(min)": measurement['result']['month_uptime'],
            "energy_today(Wh)": measurement['result']['today_energy'],
            "energy_month(Wh)": measurement['result']['month_energy']
        },
        "current_power(mW)": measurement["result"]["current_power"]
    }
    electricity_collection.insert_one(time_series_entry)

publish_local_setup()
publish_electricity_data()
client.close()
