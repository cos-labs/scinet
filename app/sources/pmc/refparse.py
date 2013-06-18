"""
"""

# Imports
import re

# Project imports
from ... import refparse
from ...util import html

class PMC(refparse.RefParse):
    
    rules = {
        'container-title-short' : '.ref-journal',
        'volume' : '.ref-vol',
    }
    
    def _parse_DOI(self):
        
        return html.parse_link(
            self.qhtml, 
            'span.crossref a',
            regex.doi
        )

    pmid_pattern = re.compile(r'pubmed/(\d+)', re.I)
    def _parse_PMID(self):
        
        return html.parse_link(
            self.qhtml, 
            'span.pubmed a',
            self.pmid_pattern
        )

    pmcid_pattern = re.compile(r'pmc/articles/pmc(\d+)', re.I)
    def _parse_PMCID(self):
        
        return html.parse_link(
            self.qhtml, 
            'span.pmc a',
            self.pmcid_pattern
        )
