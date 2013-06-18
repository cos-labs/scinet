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

def human_to_csl(name):
    """Convert HumanName to CSL-formatted JSON.

    Args:
        name : HumanName or str / unicode
    Returns:
        CSL-formatted JSON

    Examples:
    >>> csl = human_to_csl(Rafael Nadal')
    >>> csl == {'given' : 'Rafael', 'family' : 'Nadal'}
    True
    >>> csl = human_to_csl(HumanName('Rafael Nadal'))
    >>> csl == {'given' : 'Rafael', 'family' : 'Nadal'}
    True
    >>> csl = human_to_csl(HumanName('George HW de Bush'))
    >>> csl == {'given' : 'George H. W.', 'family' : 'de Bush'}
    True
    """
    # Optionally convert to nameparser.HumanName
    if not isinstance(name, HumanName):
        name = HumanName(name)

    # Initialize CSL data
    csl_data = {}
    
    # Append middle name to first
    if name.middle:
        name.first += ' ' + name.middle

    # Iterate over lookup fields
    for lookup in human_to_csl_map:
        
        # Get field and function
        field = human_to_csl_map[lookup]['field']
        fun = human_to_csl_map[lookup].get('fun', I)
        
        # Get field from name
        value = getattr(name, field)

        # Skip if empty
        if not value:
            continue

        # Apply function
        value = fun(value)
        
        # Save to CSL data
        csl_data[lookup] = value

    # Return CSL data
    return csl_data

if __name__ == '__main__':
    import doctest
    doctest.testmod()
