#!/usr/bin/env python
"""
Test script for converting standard bibtex format to Scholarly json standard
Written By: Harry Rybacki
Date: 1June13
Version: 0.2

usage: ./bibtex_to_json <bibtex file> <output json>
"""

import sys
import json

from pybtex.database.input import bibtex

# open bibtex file
parser = bibtex.Parser()
data = parser.parse_file(sys.argv[1])

# container for articles
articles = []

# iterate through each article
for id in data.entries:
    to_json = {}
    article_fields = data.entries[id].fields

    # grab required fields
    try:
        to_json.update({unicode("title"): unicode(article_fields["title"])})
        to_json.update({
            unicode("date"): unicode(article_fields["year"])})
        # handle multiple authors
        authors = []
        for author in data.entries[id].persons["author"]:
            authors.append({
                unicode('given'): unicode(author.first()[0]),
                unicode('family'): unicode(author.last()[0])
            })
        to_json.update({unicode("authors"): authors})
    except:
        continue

    # grab non-required fields available
    try:
        to_json.update({
            unicode("container-title"): unicode(article_fields["journal"])})
    except:
        pass
    try:
        to_json.update({"DOI": article_fields["doi"]})
    except:
        pass
    try:
        to_json.update({"URL": article_fields["url"]})
    except:
        pass

    articles.append(json.dumps(to_json))
    #print json.dumps(to_json)

# write output to json
with open(sys.argv[2], mode='w') as output:
    json.dump(articles, output, indent=2)

