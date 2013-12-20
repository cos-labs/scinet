import bson
import json
import os

def store_json_to_file(contents, filename):
    """stores a JSON file to local storage

    :param contents: Contents of JSON to be stored
    :param filename: Filename contents will be saved to
    """
    _file = os.path.join(os.getcwd(), "app/raw", filename)
    with open(_file, "w") as fp: 
        json.dump(contents, fp, indent=4)

def get_id():
    """generates BSON ObjectID

    :return: string representation of a ObjectID
    """
    return str(bson.ObjectId())

def raw_article_exists(target_hash, target_db):
    """returns number of articles in raw with a hash

    :param target_hash: hash to check against
    :return: count of articles with target_hash
    """
    return target_db.raw.find({'hash': target_hash}).count()
