"""
DB that interacts with the articles MongoDB
Author: Harry Rybacki
Date: 5June13
"""

from pymongo import MongoClient


class DB:
    """ class representing pymongo articles DB object """

    def __init__(self, host="localhost", port=27017):
        """connects to mongoDB and respective collections"""
        client = MongoClient(host, port)
        self.db = client.crowdscholar_articles_db
        self.users = self.db.users
        self.articles = self.db.articles

    # need to add an add/validate method

    #@ todo implement
    def add(self, submission):
        """ adds submission to articles db """
        # add data
        id = self.articles.insert(submission)
        print str(id) + " added to crowdscholar_articles_db"
        return id
