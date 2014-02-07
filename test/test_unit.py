from __future__ import absolute_import
import unittest

from test.base import DbTestCase
from crowdscholar import json_controller

class TestJSONController(DbTestCase):

	def test_we_have_db(self):
		# self._client is the MongoClient instance
		assert self._client.port == 27017

	def test_init(self):
		controller = json_controller.JSONController(submission='pew', db=self._client.test, _id=1234)
		assert controller


if __name__ == '__main__':
    unittest.main()