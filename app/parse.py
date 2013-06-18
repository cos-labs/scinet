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
        # Initialize data
        data = {}

        # Extract data from lookup fields
        data.update(self.parse_lookup_fields())
        
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

            # Call method
            value = method[1]()

            # Update data if result is dict
            if isinstance(value, dict):
                data.update(
                    {k:value[k] for k in value if value[k]}
                )
            # Else store value in data
            else:
                # Get method name
                field = method[0]\
                    .replace('_parse_', '')\
                    .replace('_', '-')
                # Store value if truthy
                if value:
                    data[field] = value

        # Return extracted fields
        return data

    def parse_lookup_fields(self):
        """ 
        """
        # Quit if no lookups or no fetch
        if not hasattr(self, 'lookups') or \
                not hasattr(self, 'fetch'):
            return {}
        
        # Fetch info from data
        return self.fetch(self.data)\
            .fetch(self.lookups)
