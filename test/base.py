# helpers.py
import unittest
import os

from pymongo import MongoClient

class DbTestCase(unittest.TestCase):
	"""A TestCase that uses a temporary MongoDB database"""

	db_name = os.environ.get('TEST_DB_NAME', 'testcrowdscholar')
	db_host = os.environ.get('TEST_MONGO_HOST', 'localhost')
	db_port = int(os.environ.get('TEST_MONGO_PORT', '27017'))

	@classmethod
	def setUpClass(klass):
		'''Set up a temporary db.'''
		klass._client = MongoClient(host=klass.db_host, port=klass.db_port)
		klass.db = klass._client[klass.db_name]

	@classmethod
	def tearDownClass(klass):
		'''Drop db when all tests finish.'''
		klass._client.drop_database(klass.db)