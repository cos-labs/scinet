"""
DB that interacts with the raw MongoDB
Author: Harry Rybacki
Date: 5June13
"""

from pymongo import MongoClient


class DB:
    """class representing pymongo raw DB object"""

    def __init__(self, host="localhost", port=27018):
        """connects to mongoDB and respective collections"""
        client = MongoClient(host, port)
        self.db = client.crowdscholardev
        self.users = self.db.users
        self.raw = self.db.raw

    def add(self, submission):
        """adds submission to articles db
        
        :param submission: JSON object to be inserted
        
        :return: ObjectID of newly inserted object 
         """
        # add data
        id = self.raw.insert(submission)
        return id
