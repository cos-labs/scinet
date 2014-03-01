import os

from flask import Flask

# Setup app
app = Flask(__name__)

# Load config
app.config.from_pyfile('development_config.py')

# Import views
from views import *
if __name__ == '__main__':
    app.run()
