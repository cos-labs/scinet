"""
"""

def page_to_csl(frst, last=None):
    """Consume first and optional last page and produce
    CSL-formatted page range.

    """
    # Quit if no first page
    if not frst:
        return
    
    # Return first if not last
    # Return as a dictionary so that field is named
    # 'page', not 'pages'
    if not last:
        return {'page' : frst}
    
    # Return combined page string
    return {
        'pages' : '{0}-{1}'.format(frst, last)
    }
