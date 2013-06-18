"""
"""

# Imports
import json

# Project imports
import parse
from util import magic
from util import lookup
from util import jsontools

LR = lookup.LookupRule

@magic.regify
class CitParse(parse.Parse):
    
    def __init__(self, data):
        """ Initialize and store data. """
        self.data = jsontools.to_json(data)
    
    # Lookup rules
    lookups = {
        'title' : LR('title'),
        'container-title' : LR('journal_title'),
        'container-title-short' : LR('journal_abbrev'),
        'volume' : LR('volume'),
        'issue' : LR('issue'),
        'PMID' : LR('pmid'),
        'DOI' : LR('doi'),
    }
    
    # Fetch class for lookups
    fetch = lookup.DictFetch
