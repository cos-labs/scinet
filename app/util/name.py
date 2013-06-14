"""
"""

# Imports
from nameparser import HumanName

# Project imports
import regex

# Identity function
I = lambda i: i

human_to_csl_map = {
    'given' : {
        'field' : 'first',
        'fun' : regex.dotify,
    },
    'family' : {
        'field' : 'last',
    },
    'suffix' : {
        'field' : 'suffix',
        'fun' : lambda str: str.replace('.', ''),
    },
}

def human_to_csl(human_name):
    """Convert nameparser.HumanName to CSL-formatted JSON.

    Args:
        human_name : nameparser.HumanName
    Returns:
        CSL-formatted JSON

    Examples:
    >>> csl = human_to_csl(HumanName('Rafael Nadal'))
    >>> csl == {'given' : 'Rafael', 'family' : 'Nadal'}
    True
    >>> csl = human_to_csl(HumanName('George HW de Bush'))
    >>> csl == {'given' : 'George H. W.', 'family' : 'de Bush'}
    True
    """
    # Initialize CSL data
    csl_data = {}
    
    # Append middle name to first
    if human_name.middle:
        human_name.first += ' ' + human_name.middle

    # Iterate over lookup fields
    for lookup in human_to_csl_map:
        
        # Get field and function
        field = human_to_csl_map[lookup]['field']
        fun = human_to_csl_map[lookup].get('fun', I)
        
        # Get field from name
        value = getattr(human_name, field)

        # Skip if empty
        if not value:
            continue

        # Apply function
        value = fun(value)
        
        # Save to CSL data
        csl_data[lookup] = value

    # Return CSL data
    return csl_data

def clean_name(name):
    
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
