"""
routes file for handling get/post request for crowdscholar
Author: Harry Rybacki
Date: 5June13
"""

import json

import raw_db
import articles_db
import parser
import validator

from flask import render_template, flash, redirect, request, url_for, Response
from app import app

# connect to the database
articles_db = articles_db.DB(host="localhost", port=27017)
raw_db = raw_db.DB(host="localhost", port=27018)

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
        if not validator.articles_endpoint_validate(user_submission):
            # return error
            # @todo return specific information about failure not validating?
            return Response(status=405)

        # add meta-data to user submission -- headers and what not
        # @todo user submission is a string at this point. Need to make it a string.
        user_submission = json.loads(user_submission)
        # @todo find proper way to append request.headers to the json
        # user_submission['headers'] = request.headers
        print "####################"
        print type(request.headers)
        print request.headers.__dict__

        # add parsed data to DB
        # @todo write database hook
        # @todo create separate db instance for articles
        submission_id = articles_db.add(user_submission)

        # return URI of new resource to submitter
        #@todo: format return body with objectid?
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
        user_submission = json.loads(request.data)

        # clean or parse?
        # @todo write parser
        cleaned_data = parser.raw_endpoint_parse(user_submission)

        # add cleaned or parsed data to DB
        # @todo write database hook
        # @todo create separate db instance for raw
        submission_id = raw_db.add(cleaned_data)

        # return success message to submitter
        #@todo return any additional information?
        return Response(status=201)

    else:
        # return HTTP submission error code to user
        return Response(status=405)