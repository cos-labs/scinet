"""
"""

# Imports
import re

############
# Patterns #
############

# DOI pattern
# Taken from http://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
doi = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b')

#############
# Functions #
#############

def dotify(name):
    """Add dots after capitalized intials.

    Args:
        name : Name to dotify
    Returns:
        Name with dots after initials

    Examples:
    >>> dotify('L Ron Hubbard')
    'L. Ron Hubbard'
    >>> dotify('H G Wells')
    'H. G. Wells'
    >>> dotify('H. G. Wells')
    'H. G. Wells'
    >>> dotify('H.G. Wells')
    'H. G. Wells'
    >>> dotify('H..G. Wells')
    'H. G. Wells'

    """
    
    # Copy name to dotified
    dotified = name

    # Remove multiple contiguous dots
    dotified = re.sub('\.+', '.', dotified)
    
    # Add dots after initials
    dotified = re.sub(
        r'[A-Z](?=[\sA-Z]|$)', 
        r'\g<0>. ',
        dotified
    )

    # Add space between dots and contiguous
    # word characters: 'A.B.' -> 'A. B.'
    dotified = re.sub(
        r'[A-Z]\.(?=\w)',
        r'\g<0> ',
        dotified
    )

    # Remove extra whitespace
    dotified = re.sub('\s+', ' ', dotified)
    dotified = dotified.strip()
    
    # Return dotified name
    return dotified

# Run doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod()
