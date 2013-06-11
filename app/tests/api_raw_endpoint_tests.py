"""
Tests get/post requests for the API raw endpoint
Author: Harry Rybacki
Date: 7June13
"""

import json
import requests
import unittest


class APIRawEndpointTests(unittest.TestCase):

    def setUp(self):
        # set base url for articles endpoint
        self.url = "http://localhost:5000/raw"

    def test_get(self):
        """tests get request for raw endpoint base url against expected
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

    @unittest.skip("Not yet implemented")
    def test_post_expected_pass_files_pdf(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_files_docx(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_pass_files_html(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_pass_citebin_json(self):
        raise NotImplementedError

    def test_post_expected_pass_citelet_json(self):
        """tests post request for raw endpoint base url against expected
         response code: 201.
        """
        headers = {'content-type': 'application/json'}
        with open('citelet_valid_sample_highwire.json') as test_data:
            payload = json.load(test_data)

            # retrieve (post) request
            response = requests.post(self.url, data=json.dumps(payload),
                                     headers=headers)

            # assert post request returns a status code 201 (successly created)
            self.assertEqual(response.status_code, 201)

    @unittest.skip("Not yet implemented")
    def test_post_expected_fail_files_pdf(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_fail_files_docx(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_fail_files_html(self):
        raise NotImplementedError

    @unittest.skip("Not yet implemented")
    def test_post_expected_fail_citebin_json(self):
        raise NotImplementedError

    #@unittest.skip("Not yet implemented")
    def test_post_expected_fail_citelet_json(self):
        """tests post request for raw endpoint base url against expected
         response code: 405.
        """
        headers = {'content-type': 'application/json'}
        with open('citelet_invalid_sample_highwire.json') as test_data:
            payload = json.load(test_data)

            # retrieve (post) request
            response = requests.post(self.url, data=json.dumps(payload),
                                     headers=headers)

            # assert post request returns a status code 405 (user submission error)
            self.assertEqual(response.status_code, 405)
