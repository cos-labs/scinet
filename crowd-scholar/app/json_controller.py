"""
Handles publisher detection and JSON validation/parsing/DB insertion
originating from the Scholarly API's Raw Endpoint
Author: Harry Rybacki
Date: 11June13
"""
# @todo: do we want this to create and hand a custom Response back to the API?
# @todo: consolidate this into a class method?

import os
import time
from tasks import *
from flask import Response

# Import class registries
#from gather_citparse import CitParse
#from gather_refparse import RefParse
#from gather_validate import Validate
import sciparse


class JSONController(object):
    """determines publisher type of user submission and sends it to the
     validator and parser controllers. If the submission is successfully
     validated and parsed, it is handed off to the DB Controller for insertion.

     :param submission: JSON-formatted object representing user submission
     :param db: database for storage

     :return: flask.Response object with appropriate status code
     :return: 201: created successfully
     :return: 405: user submission error
    """
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
        """calls the validate and parse methods. If successful, the insert
         method is called.

         :return: requests.Response(status=201) if creation/insertion was successful
         :return: requests.Response(status=405) if creation/insertion was unsuccessful
        """
        # queue storing user submission to local disk
        task = store_file_to_disk.delay(self.submission, os.getcwd())

        # grab the id for the task
        task_id = task.id

        # get the result from the task
        result = store_file_to_disk.AsyncResult(task_id)
        result.get()

        # get the filename returned from the task
        if result.result is not None:
            self.file_pointer = result.result
        # or return error
        else:
            print "Failed to store file locally, app/json_controller.py"
            return Response(status=405)

        # if user submission is valid
        try:
            self.validate()
        except:
            return Response(status=405)

        # parse the submission
        parsed_submission = self.parse()

        # and insert it into the database
        submission_id = self.insert(parsed_submission)
        # if successful return successful response
        if submission_id is not None:
            return Response(status=201)
        # otherwise return server error response
        else:
            return Response(status=500)
        #return Response(status=201)
        
    def detect_publisher(self):
        """detects the publisher type of a user submission

         :return: String - publisher type
         :return:  Response with user submission error code if publisher type does not exist
        """
        try:
            return self.submission['publisher']
        except:
            return Response(status=400)

    def validate(self):
        """calls the validaton_controller on a user submission

         :return: True - if validation is successful
         :return: False - if validation is unsuccessful
        """

        # @todo: reimplement
        """
        # Look up validatation class
        validate_klass = Validate.get(self.publisher)

        # Instantiate validation class
        validate_instance = validate_klass(self.submission)

        # Validate
        validate_instance.validate()
        """
        return True

    def parse(self):
        """calls parsing_controller on a user submission

         :return: Scholarly standard JSON if parsing successful
         :return: Response with server error code if unable to be parsed
        """
        
        # initialize submission result
        result = {}

        # Look up classes
        cit_parse_klass = sciparse.CitParse.get(self.publisher)
        ref_parse_klass = sciparse.RefParse.get(self.publisher)
        # Instantiate meta parse class
        if cit_parse_klass is not None:
            cit_parse_instance = cit_parse_klass(self.submission['citation'])
            # Parse citation
            citation = cit_parse_instance.parse()
            result['citation'] = citation
        # publisher we have not created a publisher for
        else:
            # @todo:
            pass

        # Initialize references
        references = []
        
        # parse and populate references
        if ref_parse_klass is not None:
            # Parse references
            for cited_ref in self.submission['references']:
                ref_parse_instance = ref_parse_klass(cited_ref)
                reference = ref_parse_instance.parse()
                references.append(reference)
                result['references'] = references
        else:
            # @todo:  
            pass
        
        # Build result
        result['meta-data'] = self.submission['meta']
        result['_id'] = self.file_pointer
        result['hash'] = self.submission.get('hash')
        #@TODO: Expand meta-data

        return result

    def insert(self, parsed_submission):
        """queues inserting parsed submission into raw db

         :return: ObjectID - if insertion was successful
         :return: None - if insertion was unsuccessful
        """
        # @todo: pick better error statuscode
        # queue storing user submission in MongoDB 
        try:
            task = store_file_to_mongodb.delay(parsed_submission, database='crowdscholardev', collection='raw')
        # if fails, print excepton message and return error statuscode
        except Exception as e:
            print type(e), e.message
            return Response(status=501)
        
        # grab the id for the task
        task_id = task.id
        
        # get the result from the task
        result = store_file_to_mongodb.AsyncResult(task_id)
        result.get()
        
        # retuen the ObjectID created
        return result.result
