from __future__ import absolute_import

import bson
import json
import os
import pytest
import unittest

from test.base import BaseTestCase
from scinet import json_controller, main
from scinet.helpers.raw_endpoint import get_id, store_json_to_file
from scinet.helpers.groups import add_group, get_groups


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


class TestGroups(BaseTestCase):
    """Tests Group collection functions"""

    def setUp(self):
        """Instantiate test client for tests"""
        self.app = main.app.test_client()
        with open(os.path.join(HERE, 'fixtures/test_groups'), 'r') as fp:
            self.test_groups = json.load(fp)['groups']

    def test_add_nonexistant_group(self):
        """Asserts add_group returns ObjectID of a group that doesn't
         already exist in the collection"""
        result = add_group(self._groups_collection, "Fake University")
        assert self._groups_collection.find_one(({"group_name": "Fake University"}))["_id"]

    def test_add_existing_group(self):
        """Asserts add_group returns non of a group that already
        exists in the collection"""
        add_group(self._groups_collection, "Fake University")
        result = add_group(self._groups_collection, "Fake University")
        assert not result

    def test_get_groups(self):
        """Asserts get_groups returns a list of group names"""
        # Add test groups
        for group in self.test_groups:
            self._groups_collection.insert(group)
        groups = get_groups(self._groups_collection)
        assert self.test_groups[0] in groups


class TestJSONController(BaseTestCase):
    """JSONController tests"""
    def test_db_connection(self):
        # self._client is the MongoClient instance
        assert self._client.port == 27017

    def test_init(self):
        controller = json_controller.JSONController(submission='pew', db=self._client.test, _id=1234)
        assert controller

    # JSON controller tests
    # @todo: write these
    def test_valid_detect_publisher(self):
        """Test valid publisher returns correct name"""
        pass

    def test_invalid_detect_publisher(self):
        """Test invalid publisher returns resposne status 400"""
        pass


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