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
