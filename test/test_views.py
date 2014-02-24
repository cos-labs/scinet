from __future__ import absolute_import

import json
# Set environment to load testing config
import os
os.environ['TESTING'] = '1'
import unittest

from bs4 import BeautifulSoup
from crowdscholar import main
from test.base import BaseTestCase


class TestViews(BaseTestCase):
    """OSF SciNet view tests"""
    def setUp(self):
        """Instantiate test client for tests"""
        self.app = main.app.test_client()

    def test_db_connection(self):
        """Ensure test client's is connected to correct MongoDB"""
        assert self._client.host == self.app.application.config['DB_IP']

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

    # Ping endpoint tests
    def test_ping_nonexistant_hash(self):
        """Test status code 204 returned for non-existant hash in db"""
        nonexistant_hash = json.dumps({'hash': '1234567890'})
        response = self.app.post('/ping', data=nonexistant_hash)
        self.assertEqual(response.status_code, 204)

    #@todo: Fix this. How do we make the db in 'main' the same as the db for testing (from base.py?)
    def test_ping_existing_hash(self):
        """Test status code 201 returned for existing hash in db"""
        # Instansiate connection to test db
        #with main.app.test_request_context() as context:
            #db = main.get_db()
        # Create hash to test against and insert into test db
        existing_hash = {'hash': 'testhash'}
        self.db.raw.insert(existing_hash)
        #db.raw.insert(existing_hash)
        # Post to endpoint with test hash
        response = self.app.post('/ping', data=existing_hash)
        self.assertEqual(response.status_code, 201)

    # Raw endpoint tests
    def test_invalid_post_type(self):
        """Test status code 400 from bad conten-type on post to raw"""
        payload = {'content-type': 'bad_content-type'}
        response = self.app.post(
                                '/raw',
                                headers={'content-type': 'bad_content-type'}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_JSON(self):
        """Test status code 405 from improper JSON on post to raw"""
        response = self.app.post(
                                '/raw',
                                data="not a json",
                                content_type='application/json'
        )
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()