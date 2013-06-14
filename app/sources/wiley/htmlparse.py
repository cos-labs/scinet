"""
"""

# Imports
import re

# Project imports
from ... import htmlparse
from ...util import html
from ...util import regex

class Wiley(htmlparse.HTMLParse):
    
    lookups = {
        'title' : 'span.articleTitle',
        'container-title-short' : 'span.journalTitle',
        'year' : 'span.pubYear',
        'volume' : 'span.vol',
        'page-first' : 'span.pageFirst',
        'page-last' : 'span.pageLast',
    }
    
    def parse_author(self, author):
        
        author_regex = re.compile(r'''
            (?P<family>[\w\'\s]+?)  # Family name
            \s+                     # Whitespace
            (?P<given>[A-Z]+)       # Given name
            (?:                     # Begin non-capturing suffix
                \,\s+               # Comma + whitespace
                (?P<suffix>.+)      # Suffix
            )?                      # End non-capturing suffix
        ''', re.VERBOSE)
        
        fields = author_regex.search(author)

        # 
        if fields is None:
            return

        groupdict = fields.groupdict()
        return {key : groupdict[key] for key in groupdict if groupdict[key]}

    def _parse_author(self):
        
        parsed_authors = []

        authors = self.qhtml('span.author').map(
            lambda: PyQuery(this).text()
        )

        for author in authors:

            fields = self.parse_author(author)
            if fields:
                parsed_authors.append(fields)

        return parsed_authors
    
    def _parse_DOI(self):
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            regex.doi
        )
    
    pmid_pattern = re.compile(r'/pmed\?id=(\d+)', re.I)
    def _parse_PMID(self):
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            self.pmid_pattern
        )

    isi_pattern = re.compile(r'/isi\?id=(\d+)', re.I)
    def _parse_ISI(self):
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            self.isi_pattern
        )
