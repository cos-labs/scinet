from flask import Flask

# Setup app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Import views
from views import *

if __name__ == '__main__':
	app.run()
