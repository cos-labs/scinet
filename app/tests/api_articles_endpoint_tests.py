"""
Tests get/post requests for the API articles endpoint
Author: Harry Rybacki
Date: 7June13
"""

import json
import requests
import unittest


class APIArticlesEndpointTests(unittest.TestCase):

    def setUp(self):
        # set base url for articles endpoint
        self.url = "http://localhost:5000/articles"

    def test_get(self):
        """tests get request for articles endpoint base url against expected
         response code: 200, and expected title.
        """
        # retrieve (get) request
        response = requests.get(self.url)
        # expected title of articles endpoint
        html_title = "Crowd Scholar"

        # assert get request returns a status code 200 (success)
        self.assertTrue(response.status_code is 200)
        # assert expected title is in response body
        self.assertTrue(html_title in response.text.title())

    def test_post_expected_pass(self):
        """tests post request for articles endpoint base url with payload
         and headers expected to pass against response code: 201
        """
        # set basic JSON payload in scholarly standard format
        payload = {
            "citation": {
                "id": "item1",
                "author": [
                    {"given": "tim",
                     "family": "tom"}
                ],
                "container-title": "book",
                "title": "Pew pew noises.",
                "date": 2009
            }
        }

        # set content-type for api
        headers = {'content-type': 'application/json'}

        # retrieve (post) request
        response = requests.post(self.url, data=json.dumps(payload), headers=headers)

        # assert (post) request returns status code 201 (successfully created)
        self.assertTrue(response.status_code is 201)

    @unittest.skip("Not yet implemented")
    def test_post_expected_fail(self):
        raise NotImplementedError