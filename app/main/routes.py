# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
from flask import render_template, request
from flask_login import current_user, login_required
from app.main import main_bp
import requests


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

    url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/datalad_dataset_addition_procedure.md'
    headers = {'Content-type': 'text/html; charset=UTF-8'}
    response = requests.get(url, headers=headers)

    readmeRaw = response.text

    url = 'https://api.github.com/markdown'
    body = {
        "text": readmeRaw,
        "mode": "gfm",
        "context": "github/gollum"
    }
    response = requests.post(url, json=body)

    content = response.text.replace('user-content-','')

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

    url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/CONP_FAQ.md'
    headers = {'Content-type': 'text/html; charset=UTF-8'}
    response = requests.get(url, headers=headers)

    faqRaw = response.text

    url = 'https://api.github.com/markdown'
    body = {
        "text": faqRaw,
        "mode": "gfm",
        "context": "github/gollum"
    }
    response = requests.post(url, json=body)

    content = response.text.replace('user-content-','')

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

    return render_template('about.html', title='CONP | About', user=current_user)

