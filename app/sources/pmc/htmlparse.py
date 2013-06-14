"""
"""

# Imports
import re

# Project imports
from htmlcitparse import HTMLCitParse

class PMCCitParse(HTMLCitParse):
    
    rules = {
        'container-title-short' : '.ref-journal',
        'volume' : '.ref-vol',
    }
    
    def _parse_DOI(self):
        
        return parse_link(
            self.qhtml, 
            'span.crossref a',
            regex.doi
        )

    pmid_pattern = re.compile(r'pubmed/(\d+)', re.I)
    def _parse_PMID(self):
        
        return parse_link(
            self.qhtml, 
            'span.pubmed a',
            self.pmid_pattern
        )

    pmcid_pattern = re.compile(r'pmc/articles/pmc(\d+)', re.I)
    def _parse_PMCID(self):
        
        return parse_link(
            self.qhtml, 
            'span.pmc a',
            self.pmcid_pattern
        )
