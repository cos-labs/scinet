"""
Controller for handling raw endpoint api submission data validation requests
Author: Harry Rybacki
Date: 10June13
"""


# @todo: add remaining supported publishers
def validate(submission):

    # grab publisher's name
    try:
        publisher = submission['publisher']
    except:
        return False

    # frontiers validation
    if publisher == 'frontiers':
        # @todo: add more required fields.
        required_head_ref_fields = [unicode('journal_title'), unicode('author'),
                                    unicode('title'), unicode('publication_date')]

        # check required head_ref fields are present
        for field in required_head_ref_fields:
            if field not in submission['head_ref']:
                return False

        # check author field is populated
        if len(submission['head_ref']['author']) < 1:
            return False

        # @todo: how to validate references?

        # passed all tests
        else:
            return True

    # highwire validation
    elif publisher == 'highwire':
        # @todo: add more required fields
        required_head_ref_fields = [unicode('journal_title'), unicode('author'),
                                    unicode('Title'), unicode('Date')]

        # check required head_ref fields are present
        for field in required_head_ref_fields:
            if field not in submission['head_ref']:
                return False

        # check author field is populated
        if len(submission['head_ref']['author']) < 1:
            return False

        # @todo: how to validate references?

        # passed all tests
        else:
            return True

    # not a supported publisher
    else:
        return False

