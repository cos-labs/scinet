"""
Tests raw endpoint validator methods
Author: Harry Rybacki
Date: 10June13
"""

import json
import sys
import unittest

sys.path.append('/home/sphere/git/crowd-scholar/app')
import sources_frontiers_validator
import sources_highwire_validator


# @todo: add expected fails and modify respective invalid JSON(s)
class RawValidatorTests(unittest.TestCase):

    def test_citelet_frontiers_expected_pass(self):
        """tests raw endpoint validation on known good frontiers payload
         Expect to pass with return value of True
        """
        # open, load, and prepare frontiers payload
        with open('citelet_valid_sample_frontiers.json') as test_data:
            payload = json.load(test_data)
            self.assertTrue(sources_frontiers_validator.validate(payload))

    def test_citelet_highwire_expected_pass(self):
        """tests raw endpoint validation on known good highwire payload
         Expect to pass with return value of True
        """
        # open, load, and prepare frontiers payload
        with open('citelet_valid_sample_highwire.json') as test_data:
            payload = json.load(test_data)
            self.assertTrue(sources_highwire_validator.validate(payload))

    @unittest.skip('PLOS sample data is invalid JSON -- REPLACE')
    def test_citelet_PLOS_expected_pass(self):
        """tests raw endpoint validation on known good PLOS payload
         Expect to pass with return value of True
        """
        # open, load, and prepare frontiers payload
        #with open('citelet_valid_sample_plos.json') as test_data:
        #    payload = json.load(test_data)
        #    self.assertTrue(raw_endpoint_validator.validate(payload))

    def test_citelet_frontiers_expected_fail(self):
        """tests raw endpoint validation on known bad frontiers payload
         Missing 'author' field
         Expect to pass with return value of False
        """
        with open('citelet_invalid_sample_frontiers.json') as test_data:
            payload = json.load(test_data)
            self.assertFalse(sources_frontiers_validator.validate(payload))

    def test_citelet_highwire_expected_fail(self):
        """tests raw endpoint validation on known bad highwire payload
         Missing 'title' field
         Expect to pass with return value of False
        """
        with open('citelet_invalid_sample_highwire.json') as test_data:
            payload = json.load(test_data)
            self.assertFalse(sources_highwire_validator.validate(payload))

    @unittest.skip('Not yet implemented')
    def test_citelet_PLOS_expected_fail(self):
        """tests raw endpoint validation on known bad PLOS payload
         Expect to pass with return value of False
        """
        raise NotImplementedError