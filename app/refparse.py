"""
"""

# Imports
import urllib
from pyquery import PyQuery

# Project imports
import parse
from util import magic
from util import lookup

@magic.regify
class RefParse(parse.Parse):
    
    def __init__(self, html):
        
        # Unquote HTML (fixes occasional problems w/ DOIs)
        self.html = urllib.unquote(html)

        # Parse HTML using PyQuery
        self.qhtml = PyQuery(self.html)
    
    # Fetch class for lookups
    fetch = lookup.HTMLFetch
