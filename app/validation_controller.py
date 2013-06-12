"""
Controller for handling raw endpoint api submission data validation requests
Author: Harry Rybacki
Date: 11June13
"""

import sources_highwire_validator


def test_validation(submission, publisher=None):
    print 'validation controller called'
    if publisher == 'highwire':
        return sources_highwire_validator.validate(submission)
    else:
        print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        raise NotImplementedError