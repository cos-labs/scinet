"""
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import html
from ...util import page
from ...util import regex
from ...util import lookup

# Alias LookupRule for convenience
LR = lookup.LookupRule

class Highwire(refparse.RefParse):
    
    lookups = {
        'title' : LR('span.cit-article-title'),
        'container-title-short' : LR('abbr.cit-jnl-abbrev'),
        'volume' : LR('span.cit-vol'),
        'issued' : LR(
            'span.cit-pub-date',
            lambda year: [int(year)]
        ),
    }

    auth_lookups = {
        'family' : LR('span.cit-name-surname'),
        'given' : LR(
            'span.cit-name-given-names',
            regex.dotify
        ),
        'suffix' : LR('span.cit-name-suffix'),
    }
    
    def _parse_pages(self):
            
        # Extract page range
        frst = self.qhtml('span.cit-fpage').text()
        last = self.qhtml('span.cit-lpage').text()
        
        # 
        return page.page_to_csl(frst, last)

        # Quit if no first page
        if not frst:
            return
        
        # Extract last page
        last = self.qhtml('span.cit-lpage').text()
        
        # Return first if not last
        # Return as a dictionary so that field is named
        # 'page', not 'pages'
        if not last:
            return {'page' : frst}
        
        # Return combined page string
        return '{0}-{1}'.format(frst, last)

    # 
    extra_pattern = re.compile(r'access_num=(\d+)', re.I)

    def _parse_author(self):
        
        return self.qhtml('span.cit-auth').map(
            lambda: lookup.HTMLFetch(PyQuery(this))\
                .fetch(self.auth_lookups)
        )

    def _parse_DOI(self):
        
        return html.parse_link(
            self.qhtml, 
            'div.cit-extra a[href]',
            regex.doi
        )

    def _parse_PMID(self):
        
        return html.parse_link(
            self.qhtml,
            'a.cit-ref-sprinkles-medline',
            self.extra_pattern
        )

    def _parse_ISI(self):
        
        return html.parse_link(
            self.qhtml,
            'a.cit-ref-sprinkles-medline',
            self.extra_pattern
        )
