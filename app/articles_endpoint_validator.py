"""
Controller for handling articles endpoint api submission data validation requests
Author: Harry Rybacki
Date: 5June13
"""


def validate(submission):
    """ validates data submitted to api article endpoint matches Scholarly
    JSON standards
    """
    # Scholarly JSON standard
    required_scholarly_fields = [unicode('citation')]
    optional_scholarly_fields = [unicode('references'), unicode('metadata')]
    # CSL standard required fields
    required_csl_fields = [unicode('author'), unicode('date'),
                           unicode('title'), unicode('container-title')]

    # check required scholarly fields are in payload
    for requirement in required_scholarly_fields:
        if requirement not in submission:
            return False

    # check CSL standard fields in citation
    for requirement in required_csl_fields:
        if requirement not in submission['citation']:
            return False

    # check CSL standard fields in each reference
    if 'references' in submission:
        for reference in submission['references']:
            for requirement in required_csl_fields:
                if requirement not in reference:
                    return False

    # check for additional non-standard fields
    for field in submission:
        if field not in required_scholarly_fields and field not in optional_scholarly_fields:
            return False

    # validation tests compete; return True
    return True