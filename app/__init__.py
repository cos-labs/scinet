""" 
__init__ file loading and prepping necessary things 
"""

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
