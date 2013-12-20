#!flask/bin/python

""" execution point for Flask server """
from app import app
from pymongo import MongoClient

# initilization #
app.run(debug = True)
