import unittest
import os

from pymongo import MongoClient


class BaseTestCase(unittest.TestCase):
    """A TestCase that uses a temporary MongoDB database."""
    db_name = os.environ.get('DB_NAME', 'test_database')
    db_collection = os.environ.get('DB_COLLECTION', 'test_collection')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = int(os.environ.get('DB_PORT', '27017'))

    @classmethod
    def setUpClass(klass):
        """Set up a temporary db."""
        klass._client = MongoClient(host=klass.db_host, port=klass.db_port)
        klass.db = klass._client[klass.db_name]
        klass.collection = klass._client[klass.db_collection]

    @classmethod
    def tearDownClass(klass):
        """Drop db when all tests finish."""
        klass._client.drop_database(klass.db)