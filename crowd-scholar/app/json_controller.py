"""
Handles publisher detection and JSON validation/parsing/DB insertion
originating from the Scholarly API's Raw Endpoint
Author: Harry Rybacki
Date: 11June13
"""
# @todo: do we want this to create and hand a custom Response back to the API?
# @todo: consolidate this into a class method?


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

     :return: flask.Response object with appropriate status code
     :return: 201: created successfully
     :return: 405: user submission error
    """
    def __init__(self, submission=None, db=None, raw_file_pointer=None):
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
        # grab raw data's pointer
        if raw_file_pointer is not None:
            self.raw_file_pointer= raw_file_pointer
        else:
            raise TypeError('No raw file pointer given.')
        # determine publisher type
        self.publisher = self.detect_publisher()

    def submit(self):
        """calls the validate and parse methods. If successful, the insert
         method is called.

         :return: requests.Response(status=201) if creation/insertion was successful
         :return: requests.Response(status=405) if creation/insertion was unsuccessful
        """
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
        result['_id'] = self.raw_file_pointer
        result['hash'] = self.submission.get('hash')
        #@TODO: Expand meta-data

        return result

    def insert(self, parsed_submission):
        """calls raw_db_controller to insert parsed submission into raw db

         :return: ObjectID - if insertion was successful
         :retirn: None - if insertion was unsuccessful
        """
        submission_id = self.db.add(parsed_submission)
        return submission_id
