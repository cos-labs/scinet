"""
Controller for handling raw endpoint api submission data parsing requests
Author: Harry Rybacki
Date: 11June13
"""

import importlib
import sys


def parse(submission, publisher=None):
    if publisher is not None:
        # @todo: fix this hack
        sys.path.append('/home/sphere/git/crowd-scholar/app')
        print 'parsing controller called'

        publisher_module = 'sources.' + publisher + '.parser'
        parser = importlib.import_module(publisher_module)
        return parser.parse(submission)

        #return getattr(call, 'validate')(submission)
    else:
        raise TypeError('Publisher not provided for parsing.')