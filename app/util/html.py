"""
"""

#

def parse_link(qhtml, link_selector, pattern):
    
    # Get links
    links = qhtml(link_selector)
    
    # Iterate over links until PMID found
    for link in links:
        match = pattern.search(link.get('href', ''))
        if match:
            return match.groups()[0] 

def extract_selectors(pyq, lookups):
    """ 

    Args:
        pyq : 
        lookups : 
    Returns:
        ...
    """
    # Initialize fields
    fields = {}
    
    # Iterate over field rules
    for field in lookups:
     
        # Extract value from HTML
        lookup = lookups[field]
        value = pyq(lookup).text()
     
        # Add value if available
        if value:
            fields[field] = value

    # Return completed data
    return fields
