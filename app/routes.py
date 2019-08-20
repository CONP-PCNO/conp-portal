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

@app.route('/admin')
def admin():
    return render_template('admin.html', title='Admin')

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
