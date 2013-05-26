"""
handles get/post requests for crowd source
"""
import json
from flask import render_template, flash, redirect, request, url_for
from app import app
from db import DB

# connect to the database
db = DB()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/citebin', methods=['GET', 'POST'])
def citebin():
    """drop box for users to donate of raw or specific data for citations to our DB"""
    # if post -- convert and store citation
    if request.method == 'POST' or request.method == 'post':
        # convert post data to citation
        citation = json.loads(request.data)
        article_id = db.articles.insert(citation)
        return ""

    return render_template("citebin.html")
