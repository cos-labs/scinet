##raw->production script

# will overwrite anything in the orignal dict in conflict with something in the second dict
# @todo: handle conflicta
def merge_dicts(dict1, dict2):
	return dict(dict1.items() + dict2.items())

# set up our db environment
from pymongo import MongoClient

client = MongoClient("localhost", port=27017)
db = client.crowdscholar
raw = db.raw
production = db.production

# grab articles with a DOI to be processed from raw
#@todo fix 

articles = raw.find({'citation.DOI': {'$exists': True}})[:5]


def process(articles, raw, production):
	# for every article to be processed
	# for i in range(articles.count()):
	for article in articles:

		# skip the article if it's already been imported --What should we do with it?
#		if article["meta-data"]["flags"]["imported"] is True:
#			print "Article has already been imported"
#			continue

		# if primary citation is already in DB:
		if production.find( {"citation.DOI": article["citation"]["DOI"]} ).count() != 0:
			# merge non-overlapping fields
			print "update article doi: %s" % article["citation"]["DOI"]
			production.update(
							{"citation.DOI":article["citation"]["DOI"]}, 
							{"$set":
								{'citation':merge_dicts(
									article["citation"], 
									production.find({"citation.DOI": article["citation"]["DOI"]})[0])
								}
							}
						)
			# log
			print "Article %s already in production, need to merge:" % article["_id"] 
			
		# check references
		for reference in article["references"]:
			# if it exists, point to it
			try:
				# check DOI index
				production_reference = production.find_one({
					"citation.DOI": reference["DOI"]
				})
				if production_reference:
					production.update(
							{"citation.DOI":article["citation"]["DOI"]},
							{"$set":
								{"references":production_reference["_id"]}
							}
						)
					#production_article["references"].append(
						#production_reference["_id"]
					#)
			except KeyError:
				continue
				
			# else, create a new one
			reference_article = {}
			# @todo: add meta-data
			reference_article["citation"] = reference
			# insert it into production
			id = production.insert(reference_article)

			# append pointer to primary citation's reference list
			print "appending %s to article %s references" % (id, article["_id"])
			production.update(
							{"_id":article["_id"]},
							{"$set":
								{"references":id}
							}
						)



		# else create a new instance
		else: 
			production_article = {}
			production_article["_id"] = article["_id"]
			production_article["citation"] = article["citation"]
			production_article["references"] = []

			# check references
			for reference in article["references"]:
				# if it exists, point to it
				try:
					# check DOI index
					production_reference = production.find_one({
						"citation.DOI": reference["DOI"]
					})
					if production_reference:
						production_article["references"].append(
							production_reference["_id"]
						)
				except KeyError:
					continue
				try:
					# check PMID index
					production_reference = production.find_one({
						"citation.PMID": reference["PMID"]
					})
					if production_reference:
						production_article["references"].append(
							production_reference["_id"]
						)
				except KeyError:
					continue
				
				# else, create a new one
				reference_article = {}
				# @todo: add meta-data
				reference_article["citation"] = reference
				# add the reference article to the DB
				id = production.insert(reference_article)
				print "Reference doesn't exist, adding new one article: %s" % id
				
				# append pointer to primary citation's reference list
				production_article["references"].append(id)
			# add the new article to the DB	
			print "inserting newly created %s" % production_article
			production.insert(production_article)
		
		raw.update(
					{"_id":article["_id"]},
					{"$set":
						{'meta-data.flags.imported': True}
					}
				)