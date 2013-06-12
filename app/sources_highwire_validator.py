"""
highwire source validator
verifies JSON
Author: Harry Rybacki
Date: 11June13
"""


def validate(submission):
    print 'highwire validator called'
    # required CSL fields
    required_head_ref_fields = [unicode('journal_title'), unicode('author'),
                                unicode('Title'), unicode('Date')]

    # check required head_ref fields are present
    for field in required_head_ref_fields:
        if field not in submission['head_ref']:
            print 'Missing: ' + field
            return False

    # check author field is populated
    if len(submission['head_ref']['author']) < 1:
        return False

    # @todo: how to validate references?

    # passed all tests
    else:
        return True


    # frontiers validation
