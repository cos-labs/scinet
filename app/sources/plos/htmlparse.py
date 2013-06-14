"""
"""

# Imports
import re
from pyquery import PyQuery

# Project imports
from ... import htmlparse
from ...util import html
from ...util import regex

# @TODO: parse year

class PLOS(htmlparse.HTMLParse):
    
    meta_lookups = {
        'title' : 'title',
        'pages' : 'pages',
        'volume' : 'volume',
    }
    
    def parse_custom(self):
        """
        """
        # Extract content from <meta>
        meta_content = PyQuery(self.qhtml)('meta').attr('content')
        
        # Split into fields
        meta_parts = re.split(r'; citation_', meta_content, flags=re.I)
        
        # Initialize fields
        meta_fields = {}

        # Iterate over parts
        for meta_part in meta_parts:

            # Split part by '='
            part_split = re.split(r'(?<=citation_\w+)=', meta_part, flags=re.I)

            # Skip if number of parts != 2
            if len(part_split) != 2:
                continue
            
            # Clean key and value
            key = part_split[0].strip()
            val = part_split[0].strip()

            # 
            meta_fields[key] = val
        
        pass

        # Return parsed fields
        return meta_fields

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
