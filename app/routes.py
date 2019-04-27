import json, os
import requests
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Dataset, DatasetStats
from app.oauth import OAuthSignIn
from app.forms import SignInForm
from app.forms import SignUpForm


from sqlalchemy import func
from flask import render_template, request, flash, session, redirect, url_for, send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required

DATA_PATH = app.config['DATA_PATH']

@app.route('/')
@app.route('/public')
def public():
    return render_template('public.html', title='Home | CONP')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = SignInForm()

    if current_user.is_authenticated:
        return redirect(url_for('logged_in'))

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template('login.html', title='CONP | Log In', form=form, error=form.errors)

@app.route('/success', methods=['GET', 'POST'])
@login_required
def logged_in():
    if request.method == 'GET':
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

        return redirect(url_for('public'))

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
    form = SignUpForm()
    return render_template('register.html', title='CONP | Register', form=form)

@app.route('/register_new_user', methods=['GET', 'POST'])
def register_new_user():
    error = None
    form = SignUpForm()

    # Handle the BooleanField to check if is_pi or not
    if not 'pi' in request.form:
        is_pi = False
    elif request.form['pi']:
        is_pi = True

    if request.method == 'POST':
        # Check if passwords match
        if request.form['password1'] == request.form['password2']:
            if form.validate_on_submit():
                # Check if email already exists
                user = User.query.filter_by(email=request.form['email']).first()
                # Create new user
                if not user:
                    user = User(
                        oauth_id=request.form['orcid'],
                        username=request.form['username'],
                        email=request.form['email'],
                        is_whitelisted=False,
                        is_pi= is_pi,
                        affiliation=request.form['affiliation'],
                        expiration=datetime.now() + timedelta(6 * 365 / 12),  # 6 months
                        date_created=datetime.now(),
                        date_updated=datetime.now()
                    )
                    user.set_password(request.form['password1'])
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('index'))
            error = form.errors
        error = {'Passwords do not match'}
    return render_template('register.html', title='CONP | Register', form=form, error=error)


@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='CONP | Home', user=current_user)

@app.route('/search')
def search():

    return render_template('search.html', title='CONP | Search', user=current_user)


@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')

def get_download_path(dataset):
    if current_user.is_authenticated or dataset.is_private == False:
        return "/static/data/projects/" + dataset.download_path
    elif not current_user.is_authenticated or dataset.is_private == True:
        return "#"

@app.route('/dataset-search', methods=['GET'])
def dataset_search():
    if request.method == 'GET':

       if current_user.is_authenticated:
            authorized = True
       else:
            authorized = False

       if request.args.get('search') != '':

           term = '%' + request.args.get('search') + '%'
           d = Dataset.query.filter(func.lower(Dataset.name).like(func.lower(term))).first()

           elements = [
               {
               "authorized": authorized,
               "id": d.dataset_id,
               "title": d.name.replace("'", ""),
               "isPublic": d.is_private == True,
               "thumbnailURL": "/static/img/" + d.image,
               "imagePath": "/static/img/",
               "downloadPath": get_download_path(d),
               "downloads": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_downloads,
               "views": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_views,
               "likes": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_likes,
               "dateAdded": str(d.date_created.date()),
               "dateUpdated": str(d.date_updated.date()),
               "size": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().size,
               "files": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().files,
               "subjects": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_subjects,
               "format": d.format.replace("'", ""),
               "modalities": d.modality.replace("'", ""),
               "sources": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().sources
           }]


       elif request.args.get('search') == '':

           # Query datasets
           datasets = Dataset.query.order_by(Dataset.id).all()

           # Element input for payload
           elements = []


           # Build dataset response
           for d in datasets:

               dataset = {
                   "authorized": authorized,
                   "id": d.dataset_id,
                   "title": d.name.replace("'", ""),
                   "isPrivate": d.is_private == True,
                   "thumbnailURL": "/static/img/placeholder.png",
                   "imagePath" : "/static/img/",
                   "downloadPath": get_download_path(d),
                   "downloads": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_downloads,
                   "views": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_views,
                   "likes": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_likes,
                   "dateAdded": str(d.date_created.date()),
                   "dateUpdated": str(d.date_updated.date()),
                   "size": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().size,
                   "files": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().files,
                   "subjects": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().num_subjects,
                   "format": d.format.replace("'", ""),
                   "modalities": d.modality.replace("'", ""),
                   "sources": DatasetStats.query.filter_by(dataset_id=d.dataset_id).first().sources,
               }
               elements.append(dataset)

       # Construct payload
       payload = {
          "authorized": authorized,
          "total": 50,
          "sortKeys": [
            {
              "key": "title",
              "label": "Title"
            },
            {
               "key": "downloadPath",
               "label": "Download Path"
            },
            {
                "key": "imagePath",
                "label": "Image Path"
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
          "elements": elements
       }

    return json.dumps(payload)

@app.route('/dataset', methods=['GET','POST'])
def dataset_info():

    if request.method == 'GET':

        dataset_id = request.args.get('id')

    # Query dataset
    dataset = Dataset.query.filter_by(dataset_id=dataset_id).first()

    if current_user.is_authenticated:
        authorized = True
    else:
        authorized = False

    dataset = {
        "authorized": authorized,
        "id": dataset.dataset_id,
        "title": dataset.name.replace("'", ""),
        "isPrivate": dataset.is_private == True,
        "thumbnailURL": "/static/img/placeholder.png",
        "imagePath" : "/static/img/",
        "downloadPath": get_download_path(dataset),
        "downloads": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().num_downloads,
        "views": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().num_views,
        "likes": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().num_likes,
        "dateAdded": str(dataset.date_created.date()),
        "dateUpdated": str(dataset.date_updated.date()),
        "size": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().size,
        "files": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().files,
        "subjects": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().num_subjects,
        "format": dataset.format.replace("'", ""),
        "modalities": dataset.modality.replace("'", ""),
        "sources": DatasetStats.query.filter_by(dataset_id=dataset.dataset_id).first().sources
    }
    return render_template('dataset.html', title='CONP | Dataset', data=dataset, user=current_user)


@app.route('/download_metadata', methods=['GET','POST'])
def download_metadata():

    if request.method == 'GET':

        directory = os.path.basename(request.args.get('dataset'))
        root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/data/projects/')
        dataset_path = os.path.abspath(os.path.normpath(os.path.join(root_path, directory)))

        if not dataset_path.startswith(os.path.abspath(root_path)+os.sep):
            abort(404)
            return

        url = 'https://github.com/conpdatasets/' + directory + '/archive/master.zip'

        r = requests.get(url)
        if r.status_code == 200:
            return Response(r.content,
                            mimetype='application/zip',
                            headers={'Content-Disposition': 'attachment;filename=data.zip'})


@app.route('/share')
def share():
    return render_template('share.html', title='CONP | Share a Dataset', user=current_user)

@app.route('/tools')
def tools():
    return render_template('tools.html', title='CONP | Tools & Pipelines', user=current_user)

@app.route('/forums')
def forums():
    return render_template('forums.html', title='CONP | Forums', user=current_user)

@app.route('/profile')
def profile():
    return render_template('profile.html', title='CONP | My Profile', user=current_user)