from flask import render_template, flash, redirect
from app import app
from forms import LoginForm
from db import DB

# import db
db = DB()

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Some Dude' } # placeholder user
    posts = [ # placeholder posts
        {
            'author': {'nickname': 'Timmy'},
            'body': 'Some article title'
        },
        {
            'author': {'nickname': 'Tom'},
            'body': 'Another damned article title'
        }
    ]
    # start testing db
    import datetime
    user = {"nickname": "timmy",
            "password": "tommy",
            "date": datetime.datetime.utcnow()}
    userid = db.users.insert(user)

    # stop testing db   
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts,
        userid = userid) 

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data +'",remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
