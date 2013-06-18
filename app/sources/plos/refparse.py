"""
Reference parser for PLoS journals.
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import lookup
from ...util import misc
from ...util import regex

# Alias LookupRule for convenience
LR = lookup.LookupRule

class PLoS(refparse.RefParse):
    """ Parse HTML-formatted references from PLoS. """
    
    # Lookups for extracting reference meta-data
    # from <meta> tags
    meta_lookups = {
        'title' : LR('title'),
        'pages' : LR('pages'),
        'volume' : LR('volume'),
        'issued' : LR(
            'date',
            lambda year: [int(year)]
        ),
    }
    
    def _parse_meta_fields(self):
        """PLoS provides some reference meta-data in the 
        bioliography and more in <meta name="citation_reference" ...>
        tags. This function extracts available reference info from
        the <meta> tags. Fields in <meta>s are delimited by ';', and 
        keys and values are delimited by '=':

        <meta name="citation_reference" content="citation_title=An Indo-Pacific goby (Teleostei: Gobioidei) from West-Africa, with systematic notes on Butis and related eleotridine genera; citation_volume=23; citation_number=4; citation_pages=311-324; citation_date=1989; " />

        Returns:
            CSL-formatted reference info

        """
        # Extract content from <meta>
        meta_content = self.qhtml('meta')\
            .attr('content')\
            .strip('; ')
        
        # Split into fields
        meta_parts = re.split(
            r';(?=\scitation_)', 
            meta_content, 
            flags=re.I
        )
        
        # Initialize data
        meta_data = {}

        # Iterate over parts
        for meta_part in meta_parts:

            # Split part by '='
            part_split = re.split(r'(?<=\w)=', meta_part, flags=re.I)

            # Skip if number of parts != 2
            if len(part_split) != 2:
                continue
            
            # Get key
            key = part_split[0]

            # Remove initial 'citation_'
            key = key.replace('citation_', '')
            
            # Remove remaining whitespace
            key = key.strip()

            # Get value
            val = part_split[1].strip()

            # Add value to data
            meta_data[key] = val
        
        # Return parsed data
        return lookup.DictFetch(meta_data)\
            .fetch(self.meta_lookups)

    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return self.qhtml('ul[data-doi]').attr('data-doi')
