"""
Reference parser for Wiley journals.
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import refparse
from ...util import html
from ...util import regex
from ...util import lookup

LR = lookup.LookupRule

class Wiley(refparse.RefParse):
    
    lookups = {
        'title' : LR('span.articleTitle'),
        'container-title-short' : LR('span.journalTitle'),
        'year' : LR('span.pubYear'),
        'volume' : LR('span.vol'),
        'page-first' : LR('span.pageFirst'),
        'page-last' : LR('span.pageLast'),
    }
    
    def extract_author(self, author):
        """Extract author information from an HTML snippet.
        
        Args:
            author : HTML snippet string
        Returns:
            CSL-formatted dictionary of author info

        """
        author_regex = re.compile(r'''
            (?P<family>[\w\'\s]+?)  # Family name
            \s+                     # Whitespace
            (?P<given>[A-Z]+)       # Given name
            (?:                     # Begin non-capturing suffix
                \,\s+               # Comma + whitespace
                (?P<suffix>.+)      # Suffix
            )?                      # End non-capturing suffix
        ''', re.VERBOSE)
        
        # Search HTML snippet for author info
        match = author_regex.search(author)

        # Quit if no match
        if match is None:
            return
        
        # Extract values
        groupdict = match.groupdict()

        # Quit if no family name
        if 'family' not in groupdict:
            return
        
        # Get non-None values
        author = {key : groupdict[key] for key in groupdict 
            if groupdict[key]}

        # Dotify given names if available
        if 'given' in author:
            author['given'] = regex.dotify(author['given'])

        # Return parsed author
        return author

    def _parse_author(self):
        
        # Initialize parsed authors
        parsed_authors = []
        
        # Get author HTML snippets
        html_authors = self.qhtml('span.author').map(
            lambda: PyQuery(this).text()
        )
        
        # Extract author info for each HTML snippet
        for author in html_authors:

            fields = self.extract_author(author)
            if fields:
                parsed_authors.append(fields)
        
        # Return parsed authors
        return parsed_authors
    
    def _parse_DOI(self):
        """ Extract DOI from reference. """
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            regex.doi
        )
    
    pmid_pattern = re.compile(r'/pmed\?id=(\d+)', re.I)
    def _parse_PMID(self):
        """ Extract PMID from reference. """
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            self.pmid_pattern
        )

    isi_pattern = re.compile(r'/isi\?id=(\d+)', re.I)
    def _parse_ISI(self):
        """ Extract ISI ID from reference. """
        
        return html.parse_link(
            self.qhtml, 
            'ul.exteralReferences a[href]',
            self.isi_pattern
        )
