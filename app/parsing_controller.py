"""
Controller for handling raw endpoint api submission data parsing requests
Author: Harry Rybacki
Date: 11June13
"""

import sources_highwire_parser


def parse(submission):
    print 'parsing controller called'
    return sources_highwire_parser.parse(submission)
