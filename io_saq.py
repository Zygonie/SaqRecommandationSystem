# -*- coding: utf-8 -*-

__author__ = 'guillaume'

import json
from pymongo import MongoClient


# *****************************************
# Help function to be able to serialize
# list of wines into JSON file
# Returns a serializable version of object
# see https://freepythontips.wordpress.com/2013/08/08/storing-and-loading-data-with-json/
# *****************************************
def jdefault(o):
    return o.__dict__


# *****************************************
# Retrieve list of wines from file
# *****************************************
def retrieve_data_from_file(filename):
    with open(filename, mode='r') as f:
        my_list = json.load(f)  # [json.loads(line) for line in f]
    return my_list


# *****************************************
# Save list of wines to file
# *****************************************
def save_list(list_in):
    with open('listOfWines.json', mode='w') as outfile:
        json.dump(list_in, outfile, indent=4, default=jdefault)


# *****************************************
# Save the list from json to MongoDB database on compose.io
# *****************************************
def save_list_to_mongo():
    results = retrieve_data_from_file('listOfWines.json')
    # Get credentials
    with open('credentials.json') as data_file:
        credentials = json.load(data_file)
    # Connection with MongoClient
    uri = 'mongodb://{0}:{1}@{2}:{3}/{4}'.format(credentials.username, credentials.pwd,
                                                 credentials.url, credentials.port, credentials.bd)
    # Connection with MongoClient
    client = MongoClient(uri)
    # Getting database
    db = client.SaqRecommandation
    # Getting collection
    db.drop_collection('wines')
    collection = db.wines
    collection.insert(results)
    # for result in results:
    #     collection.insert(result)