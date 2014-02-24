sudo mongod --dbpath /Users/hrybacki/crowdscholardb/ &

from pymongo import MongoClient
from test2 import *

client = MongoClient()
db = client.crowdscholar
origin = db.clean_genetics
destination = db.production_genetics
merges = db.merges

payload = genetics.find()



count = 0
for article in payload:
	count +=1
	if count % 100:
		print count
	add_or_update(article, origin, destination, merges)

###############
from pymongo import MongoClient
from test2 import *

client = MongoClient()
db = client.crowdscholar
raw = db.raw

test = raw.find({"citation.DOI": {'$exists': True}})[:5000]
#test = raw.find({"citation.DOI": {'$exists': True}})

def process(articles, raw, production, merges):
    for article in articles:
        add_or_update(article, raw, production, merges)

%time process(test, raw, production, merges)

for article in test:
    add_or_update(article, raw, production, merges)

db.raw.update( {},  {$set:{"meta-data.flags.imported": false}},  {"multi": true}  )


# remove duplicate titles from PLOS Genetics
def get_non_duplicate_title_count():
titles = []
non_duplicate_titles = []
duplicate_titles = []
for article in genetics:
    titles.append(article['citation']['title'])
for title in titles:
    if title not in non_duplicate_titles:
        non_duplicate_titles.append(title)
    else:
    	duplicate_titles.append(title)
print "Total 'genetics' titles in raw:", len(titles)
print "Total non dupliate 'genetics' titles in raw:", len(duplicate_free_titles)

# cases found
1. Articles with fewer references
'Increased Life Span due to Calorie Restriction in Respiratory-Deficient Yeast'
2. Articles missing data within 'citatin'

# export a colection named 'collection' to 'collection.json'
mongoexport --db crowdscholar --collection collection --out collection.json
# get it to my machine
scp hairycode@scholalry:genetics.json ~/git
# import it local
mongoimport --dbpath /Users/hrybacki/crowdscholardb --db crowdscholar --collection genetics genetics.json




# working with ids
# g is the graph-tool graph of our data
# ids are a numpy array of article ids broken down via their respective cluster
g, ids = build_graph(cocitations, 5)
# now we can pull each cluster of ids into individual arrays for title extraction
ids_clust0 = ids[b.a==0]
...
ids_clustn = ids[b.a==n]

# extract titles for for every cluster
titles_clust0 = []
for id in ids_clust0:
    titles_clust0.append(genetics.find_one({'_id': ObjectId(id)})['citation']['title'])

# create dicts to store in cluster collection
db.create_collection('clusters')

cluster_ids = {'_id': 'cluster_ids'}
cluster_ids['0'] = list(ids_clust0) # can't store numpy array in mongo
...
cluster_ids['n'] = list(ids_clustn)

cluster_titles = {'_id': 'cluster_titles'}
cluster_titles['0'] = titles_clust0
...
cluster_titles['n'] = titles_clustn

# export and save the collection if you need to
$ mongoexport --db crowdscholar --collection clusters --out clusters.json
# import saved json if you need to
$ mongoimport --db crowdscholar --collection clusters clusters.json
