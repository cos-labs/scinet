"""
"""

# Imports
import json

# Project imports
import parse
from util import csl
from util import magic
from util import jsontools

@magic.regify
class MetaParse(parse.Parse):
    
    def __init__(self, data):
        """ Initialize and store data. """
        self.data = jsontools.to_json(data)
    
    # 
    lookups = {
        'title' : 'Title',
        'container-title' : 'journal_title',
        'container-title-short' : 'journal_abbrev',
        'volume' : 'volume',
        'issue' : 'issue',
        'DOI' : 'doi',
        'PMID' : 'pmid',
    }

    def parse_lookup_fields(self):
        """ 
        """
        # Quit if no lookups
        if not hasattr(self, 'lookups'):
            return
     
        # Initialize data
        data = {}
     
        # Extract fields from JSON
        for field in self.lookups:
            lookup = self.lookups[field]
            if lookup in self.data:
                data[field] = self.data[lookup][0]
     
        # Return parsed data
        return data

    # 
    issued_lookup = None

    def _parse_issued(self):
        
        # Parse date string
        try:
            return csl.date_to_csl(self.data[self.issued_lookup])
        except:
            pass
