import os

DEBUG = True
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_GROUPS_COLLECTION = os.environ.get("DB_GROUPS_COLLECTION")
DB_ARTICLES_COLLECTION = os.environ.get("DB_ARTICLES_COLLECTION")
SECRET_KEY = os.environ.get("SECRET_KEY")

"""
# Development server settings
DEBUG = False
SECRET_KEY = "12345"

# Development database settings
DB_IP = "localhost"
DB_PORT = 27017
DB_NAME = "crowdscholar"
"""