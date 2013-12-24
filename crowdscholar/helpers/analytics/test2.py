from bs4 import UnicodeDammit
import unicodedata
import time
import re

def ensure_unicode(value):
	return UnicodeDammit(value).unicode_markup

def normalize_unicode(value):
	return unicodedata.normalize("NFKD", ensure_unicode(value))\
		.encode('ascii', 'ignore')

def ensure_alphanum(value):
	return re.sub(r'\W', '', value)

# returns a cleaned, normalized, and shortened version of a name
def clean_author(name):
	short_name = ''.join(name.split()).lower()
	return normalize_unicode(short_name)

def clean_authors(names):
	return ''.join([clean_author(name['family']) for name in names if 'family' in name])

# returns a cleaned, normalized, version of a title
def clean_title(start_title):
	return ensure_alphanum(normalize_unicode(start_title).lower())

# merges two dicts; unioned items from dict2 overwrite dict1
def merge_dicts(dict1, dict2):
	return dict(dict1.items() + dict2.items())

# adds or updates an article from raw DB to production DB
def add_or_update(article, raw, production, merges):
	# if article is already in production db
	# get computed fields
	indices = {}

	# this should never happen--why does it?
	if 'citation' not in article:
		return None

	if 'title' in article['citation'] and 'author' in article['citation']:
		cleaned_title = clean_title(article['citation']['title'])
		cleaned_author = ''.join([
			clean_author(name['family'])
			for name in article['citation']['author']
			if 'family' in name
		])
		indices['cleaned_author_title'] = '_'.join([cleaned_author, cleaned_title])

	if 'PMID' in article['citation']:
		indices['PMID'] = article['citation']['PMID']
	if 'DOI' in article['citation']:
		indices['DOI'] = article['citation']['DOI']

	article['indices'] = indices

	production_article = None

	#for key, value in indices.items():
	for field in ['DOI', 'PMID', 'cleaned_author_title']:
		if field in indices:
			value = indices[field]
			production_article = production.find_one({
					'indices.{}'.format(field) : value
				})
			if production_article:
				break

	# ensure citation has not been imported
	try:
		if article["meta-data"]["flags"]["imported"] and production_article:
			return production_article["_id"]
	except KeyError:
		pass

	if production_article:
		# track merges
		merges.insert({
			"production_article_id": production_article["_id"],
			"raw_article_id": article.get("_id", None),
			"citation_dicts": {
				"production": production_article["citation"],
				"raw": article["citation"]
			}
		})
		# merge article with one in production db
		production.update(
			{"_id": production_article["_id"]},
			{"$set":
				{
					'citation': merge_dicts(
						article["citation"],
						production_article["citation"]
					),
					'indices': merge_dicts(
						indices,
						production_article.get('indices', {})
					)
				}
			}
		)
		# iterate through article.references
		id_list = []
		for reference in article.get("references", []):
			id_list.append(add_or_update({'citation': reference}, raw, production, merges))
		# append pointer for reference to article already in production DB
		production.update(
			{"_id": production_article["_id"]},
			{"$addToSet":
				{"references": {"$each": id_list}}
			}
		)

		_id = production_article["_id"]

	# else - article doesn't already exist in production DB	
	else:
		# create a new article to represent the article
		#print "creating a new article"
		production_article = {}
		# copy citation and meta-data to the article
		production_article["citation"] = article["citation"]
		production_article['indices'] = indices
		production_article['references'] = []
		production_article['meta-data'] = article.get('meta-data', {})

		# iterate through article.references
		id_list = []
		for reference in article.get("references", []):
			reference_id = add_or_update({'citation': reference}, raw, production, merges)
			if reference_id:
				id_list.append(reference_id)
		# append pointer for reference to article already in production DB
		production_article["references"] = id_list

		_id = production.insert(production_article)	
	
		# update imported tag in raw DB
		if '_id' in article:
			raw.update(
				{"_id": article["_id"]},
				{"$set": {
					"meta-data.flags.imported": True}
				}
			)

	return _id
