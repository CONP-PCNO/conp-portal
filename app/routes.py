import json, os, time
import requests
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Dataset, DatasetStats
from app.oauth import OAuthSignIn
from app.forms import SignInForm
from app.forms import SignUpForm
from app.threads import UpdatePipelineData

from sqlalchemy import func, or_
from flask import render_template, request, flash, session, redirect, url_for, send_file, Response, abort
from flask_login import current_user, login_user, logout_user, login_required

DATA_PATH = app.config['DATA_PATH']

#start updating data on startup
thr = UpdatePipelineData(path=os.path.join(os.path.expanduser('~'), ".cache", "boutiques"))
thr.start()
thr.join()

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
    if user is None:
        return redirect(url_for("register"))

    login_user(user, remember=True)
    session['active_token'] = access_token

    return redirect(url_for('logged_in'))

@app.route('/register')
def register():
    form = SignUpForm()
    return render_template('register.html', title='CONP | Register', form=form)

@app.route('/pipelines')
def pipelines():
    return render_template('pipelines.html', title='CONP | Tools & Pipelines')

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


def get_datset_logo(dataset_id):
    logos = {
        "8de99b0e-5f94-11e9-9e05-52545e9add8e" : "/static/img/loris.png",
        "0ea345b4-62cf-11e9-b202-52545e9add8e" : "/static/img/preventad.png",
        "0c1d0fe0-5240-11e9-9178-3417ebb10536" : "/static/img/perform.png",
        "86970552-6828-11e9-89e5-52545e9add8e" : "/static/img/medics.png",
        "47902f52-0d1c-11e9-9526-0242ac13001f" : "/static/img/openneuro.png",
        "eb7b9b10-56ec-11e9-af32-0800277806bd" : "/static/img/1000genomes.png"
    }
    return logos[dataset_id]

@app.route('/dataset-search', methods=['GET'])
def dataset_search():
    if request.method == 'GET':
       datasets = []

       if current_user.is_authenticated:
            authorized = True
       else:
            authorized = False


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
       for d in datasets:

           dataset = {
               "authorized": authorized,
               "id": d.dataset_id,
               "title": d.name.replace("'", ""),
               "isPrivate": d.is_private == True,
               "thumbnailURL": get_datset_logo(d.dataset_id),
               "imagePath" : "/static/img/",
               "downloadPath": "/static/data/projects/" + d.download_path,
               "URL": d.raw_data_url,
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
                "key" : "URL",
                "label" : "URL"
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
        "thumbnailURL": get_datset_logo(dataset.dataset_id),
        "imagePath" : "/static/img/",
        "downloadPath": "/static/data/projects/" + dataset.download_path,
        "URL" : dataset.raw_data_url,
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

    metadata = get_dataset_metadata_information(dataset)

    return render_template('dataset.html', title='CONP | Dataset', data=dataset, metadata=metadata, user=current_user)


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


def get_dataset_metadata_information(dataset):


    directory = os.path.basename(dataset['downloadPath'])
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/data/projects/')
    dataset_path = os.path.abspath(os.path.normpath(os.path.join(root_path, directory)))

    descriptor_path =  dataset_path + '/descriptor.json'


    with open(descriptor_path,'r') as json_file:
        data = json.load(json_file)

        payload = {
            "authors" : data['authors'],
            "description" : data['description'],
            "contact" : data['contact'],
            "version" : "1.0",
            "licenses" : data['licenses']
        }

    return payload

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

@app.route('/pipeline-search', methods=['GET'])
def pipeline_search():
    if request.method == 'GET':

        authorized = True if current_user.is_authenticated else False

        # initialize variables
        search_query = request.args.get("search").lower()
        sort_key = request.args.get("sortKey") or "downloads-desc"
        cache_dir = os.path.join(os.path.expanduser('~'), ".cache", "boutiques")
        all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
        all_detailed_desc_path = os.path.join(cache_dir, "detailed_all_descriptors.json")

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
                    (str(descriptor.values()) + str(detailed_all_descriptors[d_index]["tags"].values())).lower()
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
        elements = [{k.lower().replace("-", ""): v for k, v in element.items()} for element in elements]
        elements.sort(
            key=lambda x: x["downloads"],
            reverse=True if sort_key == "downloads-desc" or sort_key == "title" else False
        )

        # if element has online platform url, retrieve the cbrain one, else take the first one and set logo
        for element in elements:
            if "onlineplatformurls" in element:
                for url in element["onlineplatformurls"]:
                    if "cbrain" in url:
                        element["onlineplatformurls"] = url
                        element["img"] = "static/img/run_on_cbrain_green.png"
                        break
                else:
                    element["onlineplatformurls"] = element["onlineplatformurls"][0]
                    element["img"] = "static/img/globe-solid-green.svg"
            else:
                element["img"] = "static/img/globe-solid-grey.svg"

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
