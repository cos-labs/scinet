"""
"""

# Imports
from dateutil.parser import parse as dateparse
import datetime

def date_to_csl(date):
    """Convert a date (either a string or datetime.date object)
    into CSL-formatted JSON.

    Args:
        date : String or datetime.date
    Returns:
        CSL-formatted representation of date

    Examples:
    >>> csl = date_to_csl('10/1/1985')
    >>> csl == {'date-parts' : [1985, 10, 1]}
    True
    >>> csl = date_to_csl(datetime.date(1991, 10, 13))
    >>> csl == {'date-parts' : [1991, 10, 13]}
    True
    """

    if not isinstance(date, datetime.date):

        # Parse date string
        try:
            date = dateparse(date)
        except ValueError:
            return

    # Extract date parts
    date_parts = [
        date.year,
        date.month,
        date.day,
    ]

    # Return formatted date
    return {'date-parts' : date_parts}

# Run doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod()
