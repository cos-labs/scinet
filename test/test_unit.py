from __future__ import absolute_import

import bson
import os
os.environ['TESTING'] = '1'
import pytest
import unittest

from test.base import BaseTestCase
from scinet import json_controller
from scinet.helpers.raw_endpoint import get_id, store_json_to_file


HERE = os.path.dirname(os.path.abspath(__file__))

# Helper functions for unit tests
def assert_file_exists(filepath):
    try:
        with open(filepath, 'r'):
            pass
        os.remove(filepath)
    except (IOError):
        raise AssertionError('file does not exists')
    return True


def test_assert_file_exists():
    with pytest.raises(AssertionError):
        assert_file_exists('idontexists')
    # This assert is deleting the __init__.py ... dumb
    # assert assert_file_exists(os.path.join(HERE, '__init__.py')) is True


class TestJSONController(BaseTestCase):
    """JSONController tests"""
    def test_db_connection(self):
        # self._client is the MongoClient instance
        assert self._client.port == 27017

    def test_init(self):
        controller = json_controller.JSONController(submission='pew', db=self._client.test, _id=1234)
        assert controller
    '''
    # JSON controller tests
    # @todo: write these
    def test_valid_detect_publisher(self):
        """Test valid publisher returns correct name"""
        pass

    def test_invalid_detect_publisher(self):
        """Test invalid publisher returns resposne status 400"""
        pass
    '''


class TestHelperFunctions(BaseTestCase):
    """OSF SciNet library helper function tests"""
    # Helper function tests
    def test_get_ID(self):
        """Test bson ObjectID generator
        @todo: Need to complete. Can't seem to work with bson.ObjectID ...?
        """
        _id = get_id()
        assert isinstance(_id, bson.ObjectId)

    def test_store_JSON_to_file(self):
        """Test store raw JSON payload to local directory"""
        contents = {'payload': 'some stuff'}
        filepath = os.path.join(HERE, 'tmp.json')
        contents = {'payload': 'some stuff'}
        store_json_to_file(contents, filepath)
        assert_file_exists(filepath)

if __name__ == '__main__':
    unittest.main()