"""
"""

# Imports
import glob
import json
import numpy as np
from fuzzywuzzy import fuzz

# Project imports


def read_fixtures(fixture_dir):
    
    # Initialize fixtures
    fixtures = []
    
    fixture_names = glob.glob('%s/*.json' % (fixture_dir))

    for fixture_name in fixture_names:
        
        with open(fixture_name) as fp:
            fixture = json.load(fp)
            fixtures.append(fixture)

    return fixtures

unique_fields = [
    'DOI',
    'URL',
    'PMID',
    'PMCID',
]

# Identity function
I = lambda i: i

def match_factory(field, fun, access_fun=I):
    """Create a fuzzy matching function for a given field.

    Args:
        field : Name of field in record dictionary
        fun : Matching function to apply to field values
            (must take two arguments)
        access_fun : Access function for fields in record;
            defaults to identity function
    Returns:
        Matching function that takes two records

    """
    def match(record0, record1):
        
        value0 = access_fun(record0.get(field, None))
        value1 = access_fun(record1.get(field, None))
        if value0 and value1:
            return fun(value0, value1)

    return match

def access_author(author):
    """ Access function for author field. """
    
    try:
        return author[0]['family']
    except:
        pass

def access_issued(issued):
    """ Access function for issued field. """
    
    try:
        return issued['date-parts'][0][0]
    except:
        pass

fuzzy_rules = [
    match_factory('title', fuzz.token_set_ratio),
    match_factory('container-title', fuzz.token_set_ratio),
    match_factory('author', fuzz.token_set_ratio, access_author),
    match_factory('issued', fuzz.token_set_ratio, access_issued),
]

def unique_group_compare(group0, group1, unique_fields):
    """Compare two groups of records according to unique fields
    (e.g., DOI, URL). If any unique fields are shared among groups,
    they match.

    Args:
        group0 : First group of records
        group1 : Second group of records
        unique_fields : Keys to unique fields
    Returns:
        Are any unique fields shared? [bool]
    
    """
    # Iterate over fields
    for field in unique_fields:
        
        # Get values for each group
        values0 = [record[field] for record in group0 if field in record]
        values1 = [record[field] for record in group1 if field in record]
        
        # Match if intersection is not empty
        if set(values0).intersection(values1):
            return True
    
    # No match
    return False

def fuzzy_group_compare(group0, group1, fuzzy_rules):
    """Compare two groups of records using fuzzy matching. If any
    pairs of records are similar enough across gruops, they match.

    Args:
        group0 : First group of records
        group1 : Second group of records
        fuzzy_rules : List of matching rules
    Returns:
        Do any rules match? [bool]
    
    """
    
    # Iterate over first group
    for record0 in group0:
        
        # Iterate over second group
        for record1 in group1:
            
            # Initialize scores
            fuzzy_scores = []
            
            # Get score for each rule
            for fuzzy_rule in fuzzy_rules:
                
                # Get score
                fuzzy_score = fuzzy_rule(record0, record1)
                
                # Append score if not None
                if fuzzy_score is not None:
                    fuzzy_scores.append(fuzzy_score)
            
            # Match if mean is above threshold
            if np.mean(fuzzy_scores) > 75:
                return True
    
    # No match
    return False

def detect(records):
    """Detect groups of conflicted records.

    Args:
        records : list of CSL-formatted records
    Returns:
        list of lists of conflicted records

    """
    
    # Quit if no records provided
    if not records:
        return []
    
    # Set first group to array containing first record
    groups = [ [records[0]] ]

    # Iterate over remaining records
    for record in records[1:]:
        
        # Initialize grouped to False
        grouped = False
        
        # Iterate over groups
        for group in groups:
            
            # If record matches group, append
            if unique_group_compare(group, [record], unique_fields) or \
                    fuzzy_group_compare(group, [record], fuzzy_rules):
                
                # Append record to matching group
                group.append(record)
                grouped = True
                break
        
        # If record matched no groups, create new group
        if not grouped:
            groups.append( [record] )

    # Return list of non-singleton groups
    return [group for group in groups if len(group) > 1]
