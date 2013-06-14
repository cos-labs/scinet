"""
"""

# Imports
import json

def to_json(data):
    """ Ensure that data is a JSON-formatted object. """
    
    if type(data) in [dict, list]:
        return data
    return json.loads(data)
