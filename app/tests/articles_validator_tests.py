"""
Tests articles endpoint validator methods
Author: Harry Rybacki
Date: 10June13
"""

import sys
import unittest

sys.path.append('/home/sphere/git/crowd-scholar/app')
import articles_endpoint_validator


class ArticlesValidatorTests(unittest.TestCase):

    def test_citation_missing_csl_field_expected_fail(self):
        """tests articles endpoint validation with citation missing required
         field. Expect to fail with return value of False
        """
        payload = {
            "citation": {
                "id": "item1",
                "author": [
                    {"given": "tim",
                     "family": "tom"}
                ],
                "type": "book"
            }
        }

        # call articles endpoint validation on payload
        self.assertFalse(articles_endpoint_validator.validate(payload))

    def test_reference_missing_csl_field_expected_fail(self):
        """tests articles endpoint validation with citation missing required
         field. Expect to fail with return value of False
        """
        payload = {
            "citation": {
                "id": "item1",
                "title": "Some article about domokuns.",
                "author": [
                    {"given": "tim",
                     "family": "tom"}
                ],
                "type": "book"
            },

            "references": [
                {
                    "id": "item2",
                    "author": [
                        {"given": "chevy",
                         "family": "chaser"}
                    ],
                    "type": "book"
                }
            ]
        }

        # call articles endpoint validation on payload
        self.assertFalse(articles_endpoint_validator.validate(payload))

    def test_payload_missing_scholarly_field_expected_fail(self):
        """tests articles endpoint validation missing a Scholary required
         field. Expect to fail with return value of False
        """
        payload = {
            "references": [
                {
                    "id": "item2",
                    "title": "Some older article about some domokuns.",
                    "author": [
                        {"given": "chevy",
                         "family": "chaser"}
                    ],
                    "type": "book"
                },
                {
                    "id": "item3",
                    "title": "Some article about some domokun lovers.",
                    "author": [
                        {"given": "kim",
                         "family": "possibly"}
                    ],
                    "type": "book",
                    "doi":  "asdflkj209asdlkfj209sadfkj2"
                }
            ]
        }

        # call articles endpoint validation on payload
        self.assertFalse(articles_endpoint_validator.validate(payload))

    def test_payload_without_references_expected_pass(self):
        """tests articles endpoint validation on known good payload without
         references. Expect to pass with return value of True
        """
        payload = {
            "citation": {
                "id": "item1",
                "title": "Some article about domokuns.",
                "author": [
                    {"given": "tim",
                     "family": "tom"}
                ],
                "type": "book"
            }
        }

        # call articles endpoint validation on payload
        self.assertTrue(articles_endpoint_validator.validate(payload))

    def test_payload_with_references_expected_pass(self):
        """tests articles endpoint validation on known good payload with
         references. Expect to pass with return value of True
        """
        payload = {
            "citation": {
                "id": "item1",
                "title": "Some article about domokuns.",
                "author": [
                    {"given": "tim",
                     "family": "tom"}
                ],
                "type": "book"
            },

            "references": [
                {
                    "id": "item2",
                    "title": "Some older article about some domokuns.",
                    "author": [
                        {"given": "chevy",
                         "family": "chaser"}
                    ],
                    "type": "book"
                },
                {
                    "id": "item3",
                    "title": "Some article about some domokun lovers.",
                    "author": [
                        {"given": "kim",
                         "family": "possibly"}
                    ],
                    "type": "book",
                    "doi":  "asdflkj209asdlkfj209sadfkj2"
                },
                {
                    "id": "item4",
                    "title": "Some article about some people who made their fortunes from selling domokuns.",
                    "author": [
                        {"given": "lyla",
                         "family": "lilly"},
                        {"given": "jimmy",
                         "family": "jaseper"}
                    ],
                    "type": "webpage",
                    "url":  "http://www.pewpew.com/domokun_seller_gets_rich"
                }
            ],

            "metadata": {
                "source": "some submitter",
                "parse_style": "manual / parscite / scraping"
            }
        }

        # call articles endpoint validation on payload
        self.assertTrue(articles_endpoint_validator.validate(payload))
