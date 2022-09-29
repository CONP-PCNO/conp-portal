# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
import os
import json
from urllib import request
from urllib.parse import urlparse

from flask import render_template, redirect, abort
from flask import current_app
from flask import request as flask_request
from flask_login import current_user
from app.main import main_bp
from app.models import Dataset
from app.services import github


@main_bp.route('/')
@main_bp.route('/index')
def index():
    """ Index Route

        The route to the non-public index page

        Args:
            None

        Returns:
            The rendered index.html template for the current_user
    """

    return render_template('index.html', title='CONP | Home', user=current_user)


@main_bp.route('/share')
def share():
    """ Share Route

        Route to lead to the share page

        Args:
            None

        Returns:
            rendered template for share.html
    """

    content = github.get_share_content()

    return render_template('share.html', title='CONP | Share a Dataset', user=current_user, content=content)


@main_bp.route('/faq')
def faq():
    """ FAQ Route

        Route to lead to the faq page

        Args:
            None

        Returns:
            rendered template for faq.html
    """

    content = github.get_faq_content()

    return render_template('faq.html', title='CONP | FAQ', user=current_user, content=content)


@main_bp.route('/contact_us')
def contact_us():
    """ Contact Us Route

        Route to lead to the contact page

        Args:
            None

        Returns:
            rendered template for contact_us.html
    """

    return render_template('contact_us.html', title='CONP | Contact Us', user=current_user)


@main_bp.route('/about')
def about():
    """ About Route

        Route to lead to the about page

        Args:
            None

        Returns:
            rendered template for about.html
    """

    # count number of datasets
    datasets = Dataset.query.order_by(Dataset.id).all()
    countDatasets = len(datasets)

    # count number of pipelines
    cache_dir = os.path.join(os.path.expanduser(
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")

    with open(all_desc_path, "r") as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path, "r") as f:
        detailed_all_descriptors = json.load(f)

    elements = [
        {**descriptor, **detailed_all_descriptors[d_index]}
        for d_index, descriptor in enumerate(all_descriptors)
    ]

    # filter out the deprecated pipelines
    elements = list(filter(lambda e: (not e["DEPRECATED"]), elements))

    countPipelines = len(elements)

    return render_template('about.html', title='CONP | About', user=current_user,
                           countDatasets=countDatasets, countPipelines=countPipelines)


@main_bp.route('/team')
def team():
    """ Team Route

        Route to lead to the team page

        Args:
            None

        Returns:
            rendered template for team.html
    """
    return render_template('team.html', title='CONP | Developer Team', user=current_user)


@main_bp.route('/tutorial')
def tutorial():
    """ Tutorial Route

        Route to lead to the tutorial page

        Args:
            None

        Returns:
            rendered template for tutorial.html
    """

    content = github.get_tutorial_content()

    return render_template('tutorial.html', title='CONP | Tutorial', user=current_user, content=content)


@main_bp.route('/dats-editor')
def dats_editor():
    """ DATS Editor Route

        Route to lead to the DATS Editor page

        Args:
            None
        Returns:
            rendered template for dats-editor.html
    """

    content = github.get_tutorial_content()

    return render_template('dats-editor.html', title='CONP | DATS Editor', user=current_user, content=content)


@main_bp.route('/ark:/<url_naan>/<url_ark_id>')
def redirect_ark_ids(url_naan, url_ark_id):

    from flask import current_app
    from app import db
    from app.models import ArkId

    config_naan = current_app.config['ARK_CONP_NAAN']
    if config_naan != url_naan:
        abort(
            404,
            f"Invalid NAAN - The NAAN portion ({url_naan}) of the provided ARK "
            f" ID does not match the portal's NAAN ({config_naan})."
        )

    requested_full_ark_id = f"ark:/{url_naan}/{url_ark_id}"
    redirect_url = None

    if url_ark_id.startswith('d7'):
        db_entry = db.session.query(ArkId.dataset_id).filter_by(
            ark_id=requested_full_ark_id
        ).first()
        redirect_url = f'/dataset?id={db_entry[0]}'
    elif url_ark_id.startswith('p7'):
        db_entry = db.session.query(ArkId.pipeline_id).filter_by(
            ark_id=requested_full_ark_id
        ).first()
        redirect_url = f'/pipeline?id={db_entry[0]}'

    if not redirect_url:
        abort(
            404,
            f'The provided ARK ID {requested_full_ark_id} does not match any '
            f' dataset or pipeline from the CONP portal. Please verify the URL.'
        )

    return redirect(redirect_url)


@main_bp.route("/cbrainredirect")
def redirect_to_cbrain():
    try:
        cbrain_url = flask_request.args["cbrainurl"]
    except KeyError:
        return redirect("/")

    parse_result = urlparse(cbrain_url)
    if (
        (parse_result.scheme != "https")
        or (parse_result.netloc != "portal.cbrain.mcgill.ca")
    ):
        return redirect("/")
    return redirect(cbrain_url)
