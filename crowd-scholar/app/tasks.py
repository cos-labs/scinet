from __future__ import absolute_import

from app.celery import celery
from pymongo import MongoClient

import bson
import json
import os

@celery.task
def store_file_to_disk(payload, directory):
    """stores a file to a local disk

    :param payload: payload to be saved
    :param directory: location to store
    
    :retun: filename if successful, None if unsuccessful
    """
    filename = str(bson.ObjectId())
    file_path = os.path.join(directory, "app/raw", filename)
    
    try:
        with open(file_path, "w") as fp:
            json.dump(payload, fp, indent=4)
        return filename
    except:
        return filename
    return filename

# @fixme: database insansiation uses hardcoded database/collection and not the parameters. How to fix?
@celery.task
def store_file_to_mongodb(payload, host='localhost', port=27017, database=None, collection=None):
    """calls raw_db_controller to insert parsed submission into raw db

     :return: ObjectID - if insertion was successful
     :retirn: None - if insertion was unsuccessful
    """
    # @todo: check for errors
    # connect to db
    client = MongoClient(host, port)
    db = client.crowdscholardev
    collection = db.raw
    
    # insert file into db
    objectid = collection.insert(payload)

    return str(objectid)

# @todo: implement
@celery.task
def check_file_in_mongodb():
    return False

