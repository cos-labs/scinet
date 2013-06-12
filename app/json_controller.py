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


class JSONController:
    """Determines publisher type of user submission and sends it to the
     validator and parser controllers. If the submission is successfully
     validated and parsed, it is handed off to the DB Controller for insertion.

     @params:    submission = requests.request object representing user
                submission

     @returns:   requests.Response object with appropriate status code
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
        if self.validate():
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

        # else return a user submission error
        # @todo: stubbed
        else:
            print 'submit() failed'
            return Response(status=405)

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
        return validation_controller.validate(self.submission, publisher=self.publisher)

    def parse(self):
        """calls parsing_controller on a user submission

         @returns:  Scholarly standard JSON if parsing successful
                    Response with server error code if unable to be parsed

        """
        # @todo: stubbed
        return parsing_controller.parse(self.submission, publisher=self.publisher)

    def insert(self, parsed_submission):
        """calls raw_db_controller to insert parsed submission into raw db

         @returns:  ObjectID - if insertion was successful
                    None - if insertion was unsuccessful
        """
        submission_id = self.db.add(parsed_submission)
        return submission_id