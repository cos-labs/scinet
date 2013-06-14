"""
highwire source validator
verifies JSON
Author: Harry Rybacki
Date: 11June13
"""

# Project imports
from ... import validate

class Highwire(validate.Validate):
    
    required_head = [
        'title',
        'journal_title',
        'author',
        'date',
    ]
