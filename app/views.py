"""
routes file for handling get/post request for crowdscholar
Author: Harry Rybacki
Date: 5June13
"""

import json

import raw_db
import articles_db
import parser

from flask import render_template, flash, redirect, request, url_for, Response
from app import app

# connect to the database
articles_db = articles_db.DB(host="localhost", port="20717")
raw_db = raw_db.DB(host="localhost", port="27018")

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/citebin', methods=['GET', 'POST'])
def Citebin():
    """drop box for users to donate of raw or specific data for citations to
    our DB"""
    # if post -- convert and store citation
    if request.method == 'POST':
        # convert post data to citation
        citation = json.loads(request.data)
        #@todo fix this to meet new db parse/insert procedures
        #article_id = db.articles.insert(citation)
        return ""

    return render_template("citebin.html")

"""
begin API handlers
"""

@app.route('/articles', methods=['GET', 'POST'])
def ArticleEndpoint():
    """
    RESTFull API endpoint for retrieving / submitting articles
    @TODO: Switch function to pluggable view approach
    """
    if request.method == 'GET':
        # load articles endpoint informational page
        return render_template("articles.html")

    elif request.method == 'POST':
        # grab data
        user_submission = request.data

        # validate data
        if not parser.articles_endpoint_validate(user_submission):
            # return error
            # @todo return specific information about failure not validating?
            return Response(status=405)

        # parse data
        # @todo write parser
        cleaned_data = parser.article_endpoint_parse(user_submission)

        # add parsed data to DB
        # @todo write database hook
        # @todo create separate db instance for articles
        articles_db.add(cleaned_data)

        # return URI of new resource to submitter
        #@todo: return resource URI as well
        return Response(status=201)

    else:
        # return HTTP submission error code to user
        return Response(status=405)

@app.route('/raw', methods=['GET', 'POST'])
def RawEndpoint():
    """
    RESTFull API endpoint for submitting raw article data.
    @TODO: Switch function to pluggable view approach
    """
    if request.method == 'GET':
        # load raw endpoint informational page
        return render_template("raw.html")

    elif request.method == 'POST':
        # grab data
        user_submission = request.data

        # clean or parse?
        # @todo write parser
        cleaned_data = parser.raw_endpoint_parse(user_submission)

        # add cleaned or parsed data to DB
        # @todo write database hook
        # @todo create separate db instance for raw
        raw_db.add(cleaned_data)

        # return success messageto submitter
        #@todo return any additional information?
        return Response(status=201)

    else:
        # return HTTP submission error code to user
        return Response(status=405)