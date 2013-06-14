"""
"""

# Project imports
from ... import validate

class Wiley(validate.Validate):

    required_head = [
        'title',
        'journal_title',
        'author',
        'publication_date',
    ]
