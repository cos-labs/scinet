"""Various helper functions used by the raw endpoint"""

import bson
import json
import os


def get_id():
	"""Generates BSON ObjectID

	:return: Unique ObjectID hex
	"""
	return str(bson.ObjectId())

def store_json_to_file(contents, filename):
	"""Stores a JSON to local storage

	:param contents: Contents of JSON to be stored
	:param filename: Filename contents will be saved to
	"""
	_file = os.path.join(os.getcwd(), "raw_payloads", filename)
	with open(_file, 'w') as fp:
		json.dump(contents, fp, indent=4)