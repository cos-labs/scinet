"""
"""

# Imports
import urllib
from pyquery import PyQuery

# Project imports
import parse
from util import html
from util import magic

@magic.regify
class HTMLParse(parse.Parse):
    
    def __init__(self, html):
        
        # Unquote HTML (fixes occasional problems w/ DOIs)
        self.html = urllib.unquote(html)

        # Parse HTML using PyQuery
        self.qhtml = PyQuery(self.html)
    
    def parse_lookup_fields(self):
        """
        """
        # Quit if no rules
        if not hasattr(self, 'lookups'):
            return
        
        # 
        return html.extract_selectors(self.qhtml, self.lookups)
