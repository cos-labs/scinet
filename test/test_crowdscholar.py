from __future__ import absolute_import
import pytest
import bson
import json
import os
import unittest

from bs4 import BeautifulSoup
from crowdscholar import main
from crowdscholar.helpers.raw_endpoint import get_id, store_json_to_file


'''
@TODO:
Look at osf/test/basy.py's setup and teardown classes for streaminglining
the test db setup/tearDown
'''

HERE = os.path.dirname(os.path.abspath(__file__))

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

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        """Instansiates test client for tests"""
        self.app = main.app.test_client()

    def tearDown(self):
        with main.app.test_request_context():
            db = main.get_db()
            db.raw.remove()

    # General page tests
    def test_index(self):
        response = self.app.get('/', content_type='html/css')
        self.assertEqual(response.status_code, 200)
        title = BeautifulSoup(response.data).title.string
        self.assertEqual(title, "Crowd Scholar")
    
    def test_404_error(self):
        """Tests page not found error handler working correctly"""
        response = self.app.get('/non_existent_page')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
                json.loads(response.data)['error'],
                u'Page Not Found'
                )

    def test_405_error(self):
        """Test method not allowed error handler working correctly"""
        response = self.app.post('/', data=dict(temp1="1", temp2="2"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
                json.loads(response.data)['error'],
                u'Method Not Allowed'
                )
    # Database tests
    def test_database(self):
        """Test database connection methods work properly"""
        with main.app.test_request_context() as context:
            db = main.get_db()
        self.assertIsNot(context.g.mongo_client, None)
        self.assertEqual(context.g.mongo_db, db)

    # Ping endpoint tests
    def test_ping_nonexistant_hash(self):
        """Test status code 204 returned for non-existant hash in db"""
        nonexistant_hash = json.dumps({'hash': '1234567890'})
        response = self.app.post('/ping', data=nonexistant_hash)
        self.assertEqual(response.status_code, 204)

    def test_ping_existing_hash(self):
        """Test status code 201 returned for existing hash in db"""
        # Instansiate connection to test db
        with main.app.test_request_context() as context:
            db = main.get_db()
        # Create hash to test against and insert into test db
        existing_hash = {'hash': 'testhash'}
        db.raw.insert(existing_hash)
        # Post to endpoint with test hash
        response = self.app.post('/ping', data=existing_hash)
        self.assertEqual(response.status_code, 201)
        # Clean up test db
        db.raw.remove()

    # Raw endpoint tests
    def test_invalid_post_type(self):
        """Test status code 400 from bad conten-type on post to raw"""
        payload = {'content-type': 'bad_content-type'}
        response = self.app.post('/raw',
                                headers={'content-type': 'bad_content-type'})
        self.assertEqual(response.status_code, 400)

    def test_invalid_JSON(self):
        """Test status code 405 from improper JSON on post to raw"""
        response = self.app.post('/raw',
                                data="not a json",
                                content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_valid_raw_endpoint_submission(self):
        # Instansiate connection to test db
        with main.app.test_request_context() as context:
            db = main.get_db()
        # Load valid fixture and prep post payload
        fixture_name = "valid_post_from_citelet"
        fixture_path = os.path.join(HERE, 
                                    "fixtures", 
                                    fixture_name)
        print '#########################', fixture_path
        with open(fixture_path) as data_file:    
            data = json.load(data_file)
        payload = json.dumps(data)
        response = self.app.post('/raw',
                                data=payload,
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)

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
if __name__ == '__main__':
    unittest.main()
