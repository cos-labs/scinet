"""
Controller for handling raw endpoint api submission data validation requests
Author: Harry Rybacki
Date: 11June13
"""

import importlib
import sys


def validate(submission, publisher=None):
    if publisher is not None:
        # @todo: fix this hack
        sys.path.append('/home/sphere/git/crowd-scholar/app')
        print 'validation controller called'

        publisher_module = 'sources.' + publisher + '.validator'
        validator = importlib.import_module(publisher_module)
        return validator.validate(submission)

        #return getattr(call, 'validate')(submission)
    else:
        raise TypeError('Publisher not provided for validation.')