import json
import os

from flask import request, g, render_template, make_response, jsonify, Response
from helpers.raw_endpoint import get_id, store_json_to_file
from helpers.groups import get_groups
from json_controller import JSONController
from main import app
from pymongo import MongoClient, errors


HERE = os.path.dirname(os.path.abspath(__file__))


# setup database connection
def connect_client():
    """Connects to Mongo client"""
    try:
        return MongoClient(app.config['DB_HOST'], int(app.config['DB_PORT']))
    except errors.ConnectionFailure as e:
        raise e


def get_db():
    """Connects to Mongo database"""
    if not hasattr(g, 'mongo_client'):
        g.mongo_client = connect_client()
        g.mongo_db = getattr(g.mongo_client, app.config['DB_NAME'])
        g.groups_collection = g.mongo_db[os.environ.get('DB_GROUPS_COLLECTION')]
    return g.mongo_db

@app.teardown_appcontext
def close_db(error):
    """Closes connection with Mongo client"""
    if hasattr(g, 'mongo_client'):
        g.mongo_client.close()

# Begin view routes
@app.route('/')
@app.route('/index/')
def index():
    """Landing page for SciNet"""
    return render_template("index.html")

@app.route('/faq/')
def faq():
    """FAQ page for SciNet"""
    return render_template("faq.html")

@app.route('/leaderboard/')
def leaderboard():
    """Leaderboard page for SciNet"""
    get_db()
    groups = get_groups(g.groups_collection)
    return render_template("leaderboard.html", groups=groups)

@app.route('/ping', methods=['POST'])
def ping_endpoint():
    """API endpoint determines potential article hash exists in db

    :return: status code 204 -- hash not present, continue submission
    :return: status code 201 -- hash already exists, drop submission
    """
    db = get_db()
    target_hash = request.form.get('hash')
    if db.raw.find({'hash': target_hash}).count():
        return Response(status=201)
    else:
        return Response(status=204)

@app.route('/articles')
def ArticleEndpoint():
    """Eventual landing page for searching/retrieving articles"""
    if request.method == 'GET':
        return render_template("articles.html")

@app.route('/raw', methods=['POST'])
def raw_endpoint():
    """API endpoint for submitting raw article data

    :return: status code 405 - invalid JSON or invalid request type
    :return: status code 400 - unsupported content-type or invalid publisher
    :return: status code 201 - successful submission
    """
    # Ensure post's content-type is supported
    if request.headers['content-type'] == 'application/json':
        # Ensure data is a valid JSON
        try:
            user_submission = json.loads(request.data)
        except ValueError:
            return Response(status=405)
        # generate UID for new entry
        uid = get_id()
        # store incoming JSON in raw storage
        file_path = os.path.join(
                        HERE,
                        'raw_payloads',
                        str(uid)
                    )
        store_json_to_file(user_submission, file_path)
        # hand submission to controller and return Resposne
        db = get_db()
        controller_response = JSONController(user_submission, db=db, _id=uid).submit()
        return controller_response

    # User submitted an unsupported content-type
    else:
        return Response(status=400)

#@TODO: Implicit or Explicit group additions? Issue #51 comments on the issues page
#@TODO: Add form validation
@app.route('/requestnewgroup/', methods=['POST'])
def request_new_group():
    # Grab submission form data and prepare email message
    data = request.json
    msg = "Someone has request that you add {group_name} to the leaderboard \
        groups. The groups website is {group_website} and the submitter can \
        be reached at {submitter_email}.".format(
                                            group_name=data['new_group_name'],
                                            group_website=data['new_group_website'],
                                            submitter_email=data['submitter_email'])
    return Response(status=200)
    '''
    try:
        email(
            subject="SciNet: A new group has been requested",
            fro="no-reply@scinet.osf.io",
            to='harry@scinet.osf.io',
            msg=msg)
        return Response(status=200)
    except:
        return Response(status=500)
    '''

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Page Not Found' } ), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify( { 'error': 'Method Not Allowed' } ), 405)