"""
"""

# Project imports
from ... import citparse
from ...util import csl
from ...util import name
from ...util import lookup

LR = lookup.LookupRule

class Highwire(citparse.CitParse):
    
    lookups = citparse.CitParse.lookups.copy()
    lookups.update({
        'issued' : LR(
            'date',
            lambda date: csl.date_to_csl(date)
        ),
    })

    def _parse_author(self):
        
        # Quit if no author
        if 'author' not in self.data:
            return
        
        # Extract CSL-formatted name for each author
        return map(name.human_to_csl, self.data['author'])
