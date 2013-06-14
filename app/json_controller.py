"""
Handles publisher detection and JSON validation/parsing/DB insertion
originating from the Scholarly API's Raw Endpoint
Author: Harry Rybacki
Date: 11June13
"""
# @todo: do we want this to create and hand a custom Response back to the API?
# @todo: consolidate this into a class method?

import validation_controller
import parsing_controller

from flask import Response

# Import class registries
from gather_htmlparse import HTMLParse
from gather_metaparse import MetaParse
from gather_validate import Validate


class JSONController(object):
    """Determines publisher type of user submission and sends it to the
     validator and parser controllers. If the submission is successfully
     validated and parsed, it is handed off to the DB Controller for insertion.

     @params:    submission = JSON-formatted object representing user
                submission

     @returns:   flask.Response object with appropriate status code
                201: created successfully
                405: user submission error
    """
    # @todo: remove defaults, add to docs in views and switch to try/excepts
    def __init__(self, submission=None, db=None):
        # grab the submission
        if submission is not None:
            self.submission = submission
        else:
            raise TypeError('No submission given.')
        # setup the database
        if db is not None:
            self.db = db
        else:
            raise TypeError('No database instance given.')
        # determine publisher type
        self.publisher = self.detect_publisher()

    def submit(self):
        print 'json_controller.submit() called'
        """calls the validate and parse methods. If successful, the insert
         method is called.

         @returns:  requests.Response(status=201) if creation/insertion
                        was successful
                    requests.Response(status=405) if creation/insertion
                        was unsuccessful
        """
        # if user submission is valid
        try:
            self.validate()
        except:
            print 'submit() failed'
            return Response(status=405)

        # parse the submission
        parsed_submission = self.parse()

        # and insert it into the database
        submission_id = self.insert(parsed_submission)
        # if successful return successful response
        if submission_id is not None:
            print 'submit() successful '
            return Response(status=201)
        # otherwise return server error response
        else:
            print 'submit() not successful'
            return Response(status=500)


    def detect_publisher(self):
        """detects the publisher type of a user submission

         @returns:  String - publisher type
                    Response with user submission error code if publisher
                        type does not exist
        """
        try:
            return self.submission['publisher']
        except:
            return Response(status=400)

    def validate(self):
        """calls the validaton_controller on a user submission

         @returns:  True - if validation is successful
                    False - if validation is unsuccessful

        import foo
        methodToCall = getattr(foo, 'bar')
        result = methodToCall()

        As far as that goes lines 2 and three can be compressed to:

        result = getattr(foo, 'bar')()
        """

        # Look up validatation class
        validate_klass = Validate.get(self.publisher)

        # Instantiate validation class
        validate_instance = validate_klass(self.submission)

        # Validate
        validate_instance.validate()

    def parse(self):
        """calls parsing_controller on a user submission

         @returns:  Scholarly standard JSON if parsing successful
                    Response with server error code if unable to be parsed

        """
        # @todo: stubbed

        # Look up classes
        meta_parse_klass = MetaParse.get(self.publisher)
        html_parse_klass = HTMLParse.get(self.publisher)
        
        # Instantiate meta parse class
        meta_parse_instance = meta_parse_klass(self.submission['head_ref'])

        # Parse citation
        citation = meta_parse_instance.parse()
        
        # Initialize references
        references = []
        
        # Parse references
        for cited_ref in self.submission['cited_refs']:

            html_parse_instance = html_parse_klass(cited_ref)
            reference = html_parse_instance.parse()
            references.append(reference)
        
        # Build result
        result = {}
        result['citation'] = citation
        result['references'] = references
        result['meta-data'] = self.submission['meta']
        #@TODO: Expand meta-data

        return result

    def insert(self, parsed_submission):
        """calls raw_db_controller to insert parsed submission into raw db

         @returns:  ObjectID - if insertion was successful
                    None - if insertion was unsuccessful
        """
        submission_id = self.db.add(parsed_submission)
        return submission_id
