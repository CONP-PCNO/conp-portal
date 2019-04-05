from app import app
from flask import render_template, request
from app.forms import SignInForm
from app.forms import SignUpForm
import json

@app.route('/')
@app.route('/public')
def public():
    signin = SignInForm()
    signup = SignUpForm()
    return render_template('public.html', title='Home', signin=signin, signup=signup)

@app.route('/login')
def login():

    signin = SignInForm()
    signup = SignUpForm()

    #if request.method == 'POST' and form.validate():
    #    if load_user(form.username.data) is None:
    #        flash('Invalid username')
    #    else:
    #        if check_password_hash(cred.password, form.password.data):
    #            return redirect(url_for('browse'))
    #       else:
    #            flash('Invalid password')
    #return render_template('login.html', title='Login', form=form)

    return render_template('index_visitor.html', title='Log in', signin=signin, signup=signup)


@app.route('/index')
def index():
    user = {'username' : 'JB'}
    return render_template('index.html', title='Home', user=user)

@app.route('/search')
def search():
    signin = SignInForm()
    signup = SignUpForm()
    return render_template('search.html', title='Search', signin=signin, signup=signup)


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

