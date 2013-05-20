from pymongo import MongoClient

""" class representing pymongo DB object """
class DB:

    def __init__(self):
        """connects to mongoDB and respective collections"""
        client = MongoClient()
        self.db = client.crowdscholar_db
        self.users = self.db.users
        self.articles = self.db.articles

    # need to add an add/validate method