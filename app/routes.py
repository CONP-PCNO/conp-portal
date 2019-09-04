# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in the whole application
    TO DO: Need to put these in the blueprints
"""
import json
import os
import time
import requests
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Dataset, DatasetStats
from app.oauth import OAuthSignIn
from app.forms import SignInForm
from app.forms import SignUpForm
from app.threads import UpdatePipelineData
from sqlalchemy import func, or_
from flask import render_template, request, flash, session, redirect, \
                  url_for, send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required

DATA_PATH = app.config['DATA_PATH']

# start updating data on startup
THR = UpdatePipelineData(path=os.path.join(
    os.path.expanduser('~'), ".cache", "boutiques"))
THR.start()
THR.join()


@app.route('/')
@app.route('/public')
def public():
    """Public Route

        This is the route that leads to the public main page

        Args:
            None

        Returns:
            rendered public.html template
    """
    return render_template('public.html', title='Home | CONP')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Route

        This route leads to the login page.

        Args:
            None

        Returns:
            if GET returns the rendered login page
            if POST returns a validated user redirected to the
                non-public index page

        Raises:
            redirects back to login if login not valid
    """
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
    """ Success Route

        This route catches a successful login
        TO DO: This seems quite redudant

        Args:
            None

        Returns:
            redirect to non-public index page
    """
    if request.method == 'GET':
        # Protected user content can be handled here
        return redirect(url_for('index'))

    return None


@app.route('/logout')
def logout():
    """ Logout Route

        The route to log a user out of the portal

        Args:
            None

        Returns:
            redirect to the public index page
    """
    logout_user()
    return redirect(url_for('public'))

# This is the first step in the login process: the 'login with X' buttons
# should direct users here with the provider name filled in


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    """ Authorize Provider Route

        First step in OATH dance to autorize the use to a provider

        Args:
            provider for oauth

        Returns:
            oauth.authorize function if successful
            redirect to index if failed
    """
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

# This is step two. The OAuth provider then sends its reply to this route


@app.route('/callback/<provider>')
def oauth_callback(provider):
    """ Callback Provider Route

        This is the second step in the OAuth process that assigns
        a token to the session

        Args:
            provider for oauth

        Returns:
            Adds token to session if successful
            If successful and no user is assigned to the oauth_id
                redirects to register account
            If unsuccessful, returns redirect to login
    """
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
    if user is None:
        return redirect(url_for("register"))

    login_user(user, remember=True)
    session['active_token'] = access_token

    return redirect(url_for('logged_in'))


@app.route('/register')
def register():
    """ Register Route

        The route to lead to the register template

        Args:
            None

        Returns
            Rendered template for register.html
    """
    form = SignUpForm()
    return render_template('register.html', title='CONP | Register', form=form)


@app.route('/pipelines')
def pipelines():
    """ Pipelines Route

        The route that leads to the pipelines page

        Args:
            None

        Returns:
            Rendered template for pipelines.html
    """
    return render_template('pipelines.html', title='CONP | Tools & Pipelines')


@app.route('/register_new_user', methods=['GET', 'POST'])
def register_new_user():
    """ Register New User Route

        This currently registers a new user.
        TO DO: Not entirely sure this is ever called and or works
               Should redo with Flask-User

        Args:
            None

        Returns:
            if GET: the rendered register.html page
            if POST: Creates new user and returns the rendered template
    """
    error = None
    form = SignUpForm()

    # Handle the BooleanField to check if is_pi or not
    is_pi = False
    print(request.args.get("pi"))
    if request.args.get("pi") == "true":
        is_pi = True

    print(is_pi)
    if request.method == 'POST':
        # Check if passwords match
        if request.form['password'] == request.form['password2']:
            if form.validate_on_submit():
                # Check if email already exists
                user = User.query.filter_by(
                    email=request.form['email']).first()
                # Create new user
                if not user:
                    user = User(
                        oauth_id=request.form['orcid'],
                        username=request.form['username'],
                        email=request.form['email'],
                        is_whitelisted=False,
                        is_pi=is_pi,
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
    """ Index Route

        The route to the non-public index page

        Args:
            None

        Returns:
            The rendered index.html template for the current_user
    """
    if current_user.is_authenticated:
        return render_template('index.html', title='CONP | Home', user=current_user)

    return None


@app.route('/search')
def search():
    """ Search Route

        The route to lead to the search page

        Args:
            None

        Returns:
            The rendered search.html page for the current_user
    """
    return render_template('search.html', title='CONP | Search', user=current_user)


@app.route('/admin')
def admin():
    """ Admin Route

        Route that leads to the admin page
        CURRENTLY NOT WORKING
        TO DO: This needs to be checked against an admin role

        Args:
            None

        Returns:
            rendered admin.html page
    """
    return render_template('admin.html', title='Admin')


def get_datset_logo(dataset_id):
    """
        Gets data set logos that are statically stored in the portal
        TODO: This should not be static, should be a fucntion the dataset in the database

        Args:
            dataset_id: the unique identifier of the dataset

        Returns:
            path to the png file for the logo
    """

    logos = {
        "8de99b0e-5f94-11e9-9e05-52545e9add8e": "/static/img/loris.png",
        "0ea345b4-62cf-11e9-b202-52545e9add8e": "/static/img/preventad.png",
        "0c1d0fe0-5240-11e9-9178-3417ebb10536": "/static/img/perform.png",
        "86970552-6828-11e9-89e5-52545e9add8e": "/static/img/medics.png",
        "47902f52-0d1c-11e9-9526-0242ac13001f": "/static/img/openneuro.png",
        "eb7b9b10-56ec-11e9-af32-0800277806bd": "/static/img/1000genomes.png"
    }
    return logos[dataset_id]


@app.route('/dataset-search', methods=['GET'])
def dataset_search():
    """ Dataset Search Route

        This route executes a dataset search

        Args:
            search is the search term in the GET Request

        Retuns:
            JSON containing the matching datasets
    """
    if request.method == 'GET':
        datasets = []

        authorized = current_user.is_authenticated

        if request.args.get('search') != '':
            term = '%' + request.args.get('search') + '%'
            # Query datasets
            datasets = Dataset.query.filter(
                or_(func.lower(Dataset.name).like(func.lower(term)),
                    func.lower(Dataset.description).like(func.lower(term)))
            )

        elif request.args.get('search') == '':
            # Query datasets
            datasets = Dataset.query.order_by(Dataset.id).all()

        # Element input for payload
        elements = []

        # Build dataset response
        for data_element in datasets:
            dataset = {
                "authorized": authorized,
                "id": data_element.dataset_id,
                "title": data_element.name.replace("'", ""),
                "isPrivate": data_element.is_private,
                "thumbnailURL": get_datset_logo(data_element.dataset_id),
                "imagePath": "/static/img/",
                "downloadPath": "/static/data/projects/" + data_element.download_path,
                "URL": data_element.raw_data_url,
                "downloads": DatasetStats.query
                                         .filter_by(dataset_id=data_element.dataset_id)
                                         .first().num_downloads,
                "views": DatasetStats.query
                                     .filter_by(dataset_id=data_element.dataset_id)
                                     .first().num_views,
                "likes": DatasetStats.query
                                     .filter_by(dataset_id=data_element.dataset_id)
                                     .first().num_likes,
                "dateAdded": str(data_element.date_created.date()),
                "dateUpdated": str(data_element.date_updated.date()),
                "size": DatasetStats.query
                                    .filter_by(dataset_id=data_element.dataset_id)
                                    .first().size,
                "files": DatasetStats.query
                                     .filter_by(dataset_id=data_element.dataset_id)
                                     .first().files,
                "subjects": DatasetStats.query
                                        .filter_by(dataset_id=data_element.dataset_id)
                                        .first().num_subjects,
                "format": data_element.format.replace("'", ""),
                "modalities": data_element.modality.replace("'", ""),
                "sources": DatasetStats.query
                                       .filter_by(dataset_id=data_element.dataset_id)
                                       .first().sources,
            }
            elements.append(dataset)

        cursor = max(min(int(request.args.get('cursor') or 0), 0), 0)
        limit = max(min(int(request.args.get('limit') or 10), 10), 0)
        sort_key = request.args.get('sortKey') or "id"
        paginated = elements[(cursor):(cursor + limit)]
        paginated.sort(key=lambda o: o[sort_key])

        # Construct payload
        payload = {
            "authorized": authorized,
            "total": len(elements),
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
                    "key": "URL",
                    "label": "URL"
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
            "elements": paginated
        }

    return json.dumps(payload)


@app.route('/dataset', methods=['GET', 'POST'])
def dataset_info():
    """ Dataset Route

        Route to get the page for one dataset

        Args:
            id (REQ ARG): the id of the dataset to display

        Returns:
            rendered dataset.html for the dataset

    """

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
        "isPrivate": dataset.is_private,
        "thumbnailURL": get_datset_logo(dataset.dataset_id),
        "imagePath": "/static/img/",
        "downloadPath": "/static/data/projects/" + dataset.download_path,
        "URL": dataset.raw_data_url,
        "downloads": DatasetStats.query
                                 .filter_by(dataset_id=dataset.dataset_id)
                                 .first().num_downloads,
        "views": DatasetStats.query
                             .filter_by(dataset_id=dataset.dataset_id)
                             .first().num_views,
        "likes": DatasetStats.query
                             .filter_by(dataset_id=dataset.dataset_id)
                             .first().num_likes,
        "dateAdded": str(dataset.date_created.date()),
        "dateUpdated": str(dataset.date_updated.date()),
        "size": DatasetStats.query
                            .filter_by(dataset_id=dataset.dataset_id)
                            .first().size,
        "files": DatasetStats.query
                             .filter_by(dataset_id=dataset.dataset_id)
                             .first().files,
        "subjects": DatasetStats.query
                                .filter_by(dataset_id=dataset.dataset_id)
                                .first().num_subjects,
        "format": dataset.format.replace("'", ""),
        "modalities": dataset.modality.replace("'", ""),
        "sources": DatasetStats.query
                               .filter_by(dataset_id=dataset.dataset_id)
                               .first().sources
    }

    metadata = get_dataset_metadata_information(dataset)

    return render_template('dataset.html', title='CONP | Dataset',
                           data=dataset, metadata=metadata,
                           user=current_user)


@app.route('/download_metadata', methods=['GET', 'POST'])
def download_metadata():
    """ Download Metadata Route

        route to allow downloading the metadata for a dataset
        TODO: Currently allows post but does not use it

        Args:
            dataset (REQ ARG): the dataset

        Returns:
            Response to the zipped metadata for the browser to download

        Raises:
            HTML error if this fails
    """
    if request.method == 'GET':

        directory = os.path.basename(request.args.get('dataset'))
        root_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'static/data/projects/')
        dataset_path = os.path.abspath(
            os.path.normpath(os.path.join(root_path, directory)))

        if not dataset_path.startswith(os.path.abspath(root_path)+os.sep):
            abort(404)
            return

        url = 'https://github.com/conpdatasets/' + directory + '/archive/master.zip'

        r = requests.get(url)
        if r.status_code == 200:
            return Response(r.content,
                            mimetype='application/zip',
                            headers={'Content-Disposition': 'attachment;filename=data.zip'})


def get_dataset_metadata_information(dataset):
    """
        returns the datasets metadata

        Args:
            dataset: dictionary for the dataset

        Returns
            payload containing the datasets metadata

    """
    directory = os.path.basename(dataset['downloadPath'])
    root_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'static/data/projects/')
    dataset_path = os.path.abspath(
        os.path.normpath(os.path.join(root_path, directory)))

    descriptor_path = dataset_path + '/descriptor.json'

    with open(descriptor_path, 'r') as json_file:
        data = json.load(json_file)

        payload = {
            "authors": data['authors'],
            "description": data['description'],
            "contact": data['contact'],
            "version": "1.0",
            "licenses": data['licenses']
        }

    return payload


@app.route('/share')
def share():
    """ Share Route

        Route to lead to the share page
        CURRENTLY NOT WORKING

        Args:
            None

        Returns:
            rendered template for share.html
    """
    return render_template('share.html', title='CONP | Share a Dataset', user=current_user)


@app.route('/tools')
def tools():
    """ Tools Route

        Route to lead to the tools page

        Args:
            None

        Returns:
            rendered template for tools.html for current_user
    """

    return render_template('tools.html', title='CONP | Tools & Pipelines', user=current_user)


@app.route('/forums')
def forums():
    """ Forums Route

        Route to lead to the forums page
        CURRENTLY NOT WORKING

        Args:
            None

        Returns:
            rendered template for forums.html for current_user
    """
    return render_template('forums.html', title='CONP | Forums', user=current_user)


@app.route('/profile')
def profile():
    """ Profile Route

        Route to lead to the users profile page
        CURRENTLY NOT WORKING

        Args:
            None

        Returns:
            rendered template for share.html
    """

    return render_template('profile.html', title='CONP | My Profile', user=current_user)


@app.route('/pipeline-search', methods=['GET'])
def pipeline_search():
    """ Pipeline Search Route

        This route is for searching the set of pipelines in the Portal

        Args:
            search (REQ ARG): search term

        Returns:
            JSON of the applicable pipelines
    """

    if request.method == 'GET':

        authorized = True if current_user.is_authenticated else False

        # initialize variables
        search_query = request.args.get("search").lower()
        sort_key = request.args.get("sortKey") or "downloads-desc"
        cache_dir = os.path.join(
            os.path.expanduser('~'), ".cache", "boutiques")
        all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
        all_detailed_desc_path = os.path.join(
            cache_dir, "detailed_all_descriptors.json")

        # fetch data from cache
        with open(all_desc_path, "r") as f:
            all_descriptors = json.load(f)

        with open(all_detailed_desc_path, "r") as f:
            detailed_all_descriptors = json.load(f)

        # if the cache data older than 5min or 300 seconds, update in background
        delta = time.time() - os.path.getmtime(all_desc_path)
        if delta > 300:
            print("Pipeline database older than 5 minutes, updating...")
            UpdatePipelineData(path=cache_dir).start()

        # search cache with search query else return everything
        if search_query not in ("", '', None):
            elements = [
                {**descriptor, **detailed_all_descriptors[d_index]}
                for d_index, descriptor in enumerate(all_descriptors)
                if search_query in (
                    (str(descriptor.values()) +
                     str(detailed_all_descriptors[d_index]["tags"].values())).lower()
                    if "tags" in detailed_all_descriptors[d_index] else
                    str(descriptor.values()).lower()
                )
            ]
        else:
            elements = [
                {**descriptor, **detailed_all_descriptors[d_index]}
                for d_index, descriptor in enumerate(all_descriptors)
            ]

        # sort, make all keys lowercase and without hyphen
        elements = [{k.lower().replace("-", ""): v for k, v in element.items()}
                    for element in elements]
        elements.sort(
            key=lambda x: x["downloads"],
            reverse=True if sort_key == "downloads-desc" or sort_key == "title" else False
        )

        # if element has online platform url, retrieve the cbrain one, else
        # take the first one and set logo
        for element in elements:
            if "onlineplatformurls" in element:
                for url in element["onlineplatformurls"]:
                    if "cbrain" in url:
                        element["onlineplatformurls"] = url
                        element["img"] = "static/img/run_on_cbrain_green.png"
                        break
                else:
                    element["onlineplatformurls"] = element["onlineplatformurls"][0]
                    element["img"] = "static/img/globe-solid-green.png"
            else:
                element["img"] = "static/img/globe-solid-grey.png"

        # construct payload
        payload = {
            "authorized": authorized,
            "total": len(elements),
            "sortKeys": [
                {
                    "key": "downloads-desc",
                    "label": "Downloads: High to Low"
                },
                {
                    "key": "downloads-asc",
                    "label": "Downloads: Low to High"
                }
            ],
            "elements": elements
        }

        return json.dumps(payload)
