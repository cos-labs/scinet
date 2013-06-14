"""
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import htmlparse
from ...util import html
from ...util import regex

class Highwire(htmlparse.HTMLParse):
    
    lookups = {
        'title' : 'span.cit-article-title',
        'container-title-short' : 'abbr.cit-jnl-abbrev',
        'volume' : 'span.cit-vol',
        'page-first' : 'span.cit-fpage',
        'page-last' : 'span.cit-lpage',
    }

    auth_lookups = {
        'family' : 'span.cit-name-surname',
        'given' : 'span.cit-name-given-names',
        'suffix' : 'span.cit-name-suffix',
    }
    
    # 
    extra_pattern = re.compile(r'access_num=(\d+)', re.I)

    def _parse_author(self):
        
        return self.qhtml('span.cit-auth').map(
            lambda: html.extract_selectors(PyQuery(this), self.auth_lookups)
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
