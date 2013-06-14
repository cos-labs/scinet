"""
"""

# Imports
import inspect
from util import xref

class Parse(object):
    
    ping_doi = False

    def parse(self):
        """
        """       
        # Extract data from lookup fields
        data = self.parse_lookup_fields()
        
        # Extract data from custom methods
        data.update(self.parse_method_fields())
        
        # Add data from DOI if available
        if self.ping_doi and 'DOI' in data:
            doi_data = xref.doi_to_csl(data['DOI'])
            data.update(doi_data)

        # Return data
        return data
    
    def parse_method_fields(self):
        """
        """
        # Initialize fields
        data = {}

        # Get field methods
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        methods = [m for m in methods if m[0].startswith('_parse')]

        # Iterate over field methods
        for method in methods:
            field = method[0]\
                .replace('_parse_', '')\
                .replace('_', '-')
            value = method[1]()
            if value:
                data[field] = value

        # Return extracted fields
        return data

    def parse_lookup_fields(self):
        """ Returns {}; should be overridden by subclasses. """
        return {}
