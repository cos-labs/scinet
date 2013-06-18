"""
"""

# Imports
import abc

class LookupRule(object):
    
    def __init__(self, field, fun=lambda i: i):
        
        self.field = field
        self.fun = fun

class LookupFetch(object):
    
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def extract(self, lookup):
        pass
    
    def __init__(self, data):
        
        self.data = data

    def fetch(self, lookups):
        
        # Initialize fields
        fields = {}
        
        # Iterate over field rules
        for field in lookups:
            
            # Get lookup parts
            lookup = lookups[field].field
            fun = lookups[field].fun

            # Extract value from HTML
            value = self.extract(lookup)
            
            # Singleton list -> value
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
         
            # Add value if available
            if value:
                fvalue = fun(value)
                if fvalue:
                    fields[field] = fvalue
        
        # Return completed fields
        return fields

class HTMLFetch(LookupFetch):
    
    def extract(self, lookup):
        return self.data(lookup).text()

class DictFetch(LookupFetch):
    
    def extract(self, lookup):
        return self.data.get(lookup, None)
