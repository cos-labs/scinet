"""
"""

# Project imports
from util import magic
from util import jsontools

class ValidationError(Exception): pass

def check_fields(dict, fields):
    
    for field in fields:
        if field not in dict or \
                not dict[field]:
            return False
    return True

@magic.regify
class Validate(object):
    
    required = [
        'url',
        'publisher',
        'ip_addr',
        'head_ref',
        'cited_refs',
        'meta',
    ]

    def __init__(self, data):
        """ Initialize and store data to be validated.

        Args:
            data : JSON-formatted object or JSON-formatted string

        """
        self.data = jsontools.to_json(data)

    def validate(self):
        
        # Check for required fields
        if not check_fields(self.data, self.required):
            raise ValidationError

        # Check for required fields
        if hasattr(self, 'required_head'):
            if not check_fields(self.data['head_ref'], self.required_head):
                raise ValidationError
