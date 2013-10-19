"""
routes file for handling get/post request for crowdscholar
Author: Harry Rybacki
Date: 5June13
"""

import json
import raw_db

from app import app
from app.util import raw_helpers
from flask import render_template, request, Response
from json_controller import JSONController

# connect with MongoDB raw collection
raw_db = raw_db.DB(host="localhost", port=27017)

@app.route('/')
def index():
    """landing page for crowdscholar"""
    return render_template("index.html")

"""begin API handlers"""

# @todo: implement error catching (DB issues?)
@app.route('/ping', methods=['POST'])
def PingEndpoint():
    """API endpoint determines potential article hash exists in db
    
    :return: status code 201 -- hash not present, continue submission
    :return: status code 204 -- hash already exists, drop submission
    """
    # if hash article is not located, return 'no content' status
    if not raw_helpers.raw_article_exists(request.form.get('hash'), raw_db):
        return Response(status=204)

    # else, return already 'created' status
    return Response(status=201)

@app.route('/articles')
def ArticleEndpoint():
    """
    Eventual landing page for searching/retrieving articles
    """
    if request.method == 'GET':
        return render_template("articles.html")

# @todo: Should API endpoints have trailing slashes? e.g.: /raw/
@app.route('/raw', methods=['GET', 'POST'])
def RawEndpoint():
    """
    RESTFull API endpoint for submitting raw article data.
    @TODO: Switch function to pluggable view approach
    """
    if request.method == 'GET':
        return render_template("raw.html")

    elif request.method == 'POST':
        # if post's content-type is JSON
        if request.headers['content-type'] == 'application/json':
            # ensure it is a valid JSON
            try:
                user_submission = json.loads(request.data)
            # return error if not a valid JSON
            except ValueError:
                return Response(status=405)

            # generate UID for new entry
            uid = raw_helpers.get_id()
            
            # store incoming JSON in raw storage
            raw_helpers.store_json_to_file(user_submission, uid)
            
            # hand user submission to the controller and return Response
            controller_response = JSONController(user_submission, db=raw_db, raw_file_pointer=uid).submit()
            return controller_response

        # user submitted a content-type no currently supported
        else:
            return Response(status=400)

    # user tried to call an unsupported HTTP method
    else:
        return Response(status=405)
