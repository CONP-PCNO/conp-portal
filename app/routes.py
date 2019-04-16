import json

from app import app, db
from app.models import User
from app.oauth import OAuthSignIn
from app.forms import SignInForm
from app.forms import SignUpForm

from flask import render_template, request, flash, session, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/public')
def public():
    return render_template('public.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))
    return render_template('login.html', title='CONP | Log In')

@app.route('/success')
@login_required
def logged_in():
    # Protected user content can be handled here
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public'))

# This is the first step in the login process: the 'login with X' buttons
# should direct users here with the provider name filled in
@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# This is step two. The OAuth provider then sends its reply to this route
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    # This is step three. The code from the provider's reply is sent back to
    # the provider and the provider returns an authentication token
    access_token, oauth_id = oauth.callback()

    if access_token is None or oauth_id is None:
        flash('Authentication failed. Please contact an admin if '
                'this problem is persistent')
        return redirect(url_for('login'))

    user = User.query.filter_by(oauth_id=oauth_id).first()

    if not user:
        # Adds any new users directly to the database. And currently only stores
        # their ORCID ID. Probably want to change this...
        user = User(oauth_id=oauth_id)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            flash("Creating new user account failed")
            redirect(url_for("index"))

    login_user(user, remember=True)
    session['active_token'] = access_token

    return redirect(url_for('logged_in'))

@app.route('/register')
def register():
    return render_template('register.html', title='CONP | Register')

@app.route('/index')
def index():
    user = {'username' : 'JB'}
    return render_template('index.html', title='Home', user=user)

@app.route('/search')
def search():
    signin = SignInForm()
    signup = SignUpForm()
    return render_template('search.html', title='Search', signin=signin, signup=signup)

@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')

@app.route('/dataset-search', methods=['GET'])
def dataset_search():
    if request.method == 'GET':

       json_dummy_response = {
  "authorized": True,
  "total": 50,
  "sortKeys": [
    {
      "key": "title",
      "label": "Title"
    },
    {
      "key": "downloads",
      "label": "Downloads"
    },
    {
      "key": "views",
      "label": "Views"
    },
    {
      "key": "likes",
      "label": "Likes"
    },
    {
      "key": "dateAdded",
      "label": "Date Added"
    },
    {
      "key": "dateUpdated",
      "label": "Date Updated"
    },
    {
      "key": "size",
      "label": "Size"
    },
    {
      "key": "files",
      "label": "Files"
    },
    {
      "key": "subjects",
      "label": "Subjects"
    },
    {
      "key": "format",
      "label": "Format"
    },
    {
      "key": "modalities",
      "label": "Modalities"
    },
    {
      "key": "sources",
      "label": "Sources"
    }
  ],
  "elements": [
    {
      "id": "0",
      "title": "Super cool data number 1",
      "isPublic": True,
      "thumbnailURL": "/static/img/placeholder.png",
      "downloads": 42,
      "views": 24,
      "likes": 12,
      "dateAdded": "10/12/2018",
      "dateUpdated": "10/13/2018",
      "size": "800mb",
      "files": 44,
      "subjects": 30,
      "format": "BIDS",
      "modalities": "fMRI",
      "sources": 3
    },
    {
      "id": "2",
      "title": "Super cool data number 2",
      "isPublic": False,
      "thumbnailURL": "/static/img/placeholder.png",
      "downloads": 42,
      "views": 24,
      "likes": 12,
      "dateAdded": "10/12/2018",
      "dateUpdated": "10/13/2018",
      "size": "800mb",
      "files": 44,
      "subjects": 30,
      "format": "BIDS",
      "modalities": "fMRI",
      "sources": 3
    }
    ]
    }

    return json.dumps(json_dummy_response)

