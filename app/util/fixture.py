"""
Utilities for generating fixtures.
"""

# Imports
import os
import json

# Project imports
import xref
import misc

fixture_dir = 'fixtures'

fixture_dois = [
    '10.3389/fnins.2012.00149',
    '10.1016/j.neuroimage.2012.07.004',
    '10.1111/j.1467-9280.2008.02145.x',
    '10.1371/journal.pone.0029411',
    '10.1080/17470910802083167',
]

def doi_to_fixture(doi, fname):
    """ Retrieve CSL data from DOI and save to file. """

    # Retrieve CSL data
    csl = xref.doi_to_csl(doi)
    
    # Write to file
    with open(fname, 'w') as fp:
        json.dump(csl, fp, indent=4)

if __name__ == '__main__':

    # Ensure that directory exists
    misc.mkdir_p(fixture_dir)

    # Iterate over DOIs
    for doi in fixture_dois:

        # Build file name
        fname = os.path.join(
            fixture_dir,
            '%s.json' % (misc.escape_doi(doi))
        )
        
        # Save CSL data to file
        doi_to_fixture(doi, fname)
