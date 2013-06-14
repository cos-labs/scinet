"""
"""

# Project imports
from ... import validate

class PMC(validate.Validate):

    required_head = [
        'title',
        'journal_title',
        'authors',
        'date',
    ]
