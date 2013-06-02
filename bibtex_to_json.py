"""
Test script for converting standard bibtex format to Scholarly json standard
Written By: Harry Rybacki
Date: 31May13
Version: 0.1
"""

import json

from pybtex.database.input import bibtex

# open the bibtex file
parser = bibtex.Parser()
data = parser.parse_file(source_file)

composite = []

# iterate through each article
for id in data.entries:
    #print data.entries[id].fields
    to_json = {}
    article_fields = data.entries[id].fields
    try:
        to_json.update({"title": article_fields["title"]})
    except:
        continue
    try:
        to_json.update({"container-title": article_fields["journal"]})
    except:
        continue
    try:
        to_json.update({"date": article_fields["year"]})
    except:
        continue

    #try:
    #    to_json.update({"DOI": article_fields["doi"]})
    #except:
    #    continue
    #try:
    #    to_json.update({"URL": article_fields["url"]})
    #except:
    #    continue

    composite.append(json.dumps(to_json))

with open(dest_file, 'w') as output:
    json.dump(composite, output)

