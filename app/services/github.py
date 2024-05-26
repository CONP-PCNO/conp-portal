import os
import requests


def render_content(raw):
    url = 'https://api.github.com/markdown'
    body = {
        "text": raw,
        "mode": "gfm",
        "context": "github/gollum"
    }

    # Get the Github username and personal access token to authenticate the request,
    # else make the request without authentication
    github_user = os.environ.get('GITHUB_USER') or None
    github_pat = os.environ.get('GITHUB_PAT') or None

    if github_user is not None and github_pat is not None:
        response = requests.post(url, json=body, auth=(github_user, github_pat))

    else:
        response = requests.post(url, json=body)

    content = response.text.replace('user-content-', '')
    return content


def get_share_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/Share_Instruction_Page_-_New_DATS_Editor.md'
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(url, headers=headers)

        raw = response.text

        content = render_content(raw)
    except requests.exceptions.HTTPError as err:
        print("ERROR: Something went wrong retrieving the Github markdown", err)

    return content


def get_download_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/CONP_portal_tutorial.md'
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(url, headers=headers)

        raw = response.text

        content = render_content(raw)
    except requests.exceptions.HTTPError as err:
        print("ERROR: Something went wrong retrieving the Github markdown", err)

    return content


def get_faq_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/CONP_FAQ.md'
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(url, headers=headers)

        raw = response.text

        content = render_content(raw)
    except requests.exceptions.HTTPError as err:
        print("ERROR: Something went wrong retrieving the Github markdown", err)

    return content


def get_tutorial_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/CONP_portal_tutorial.md'
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(url, headers=headers)

        raw = response.text

        content = render_content(raw)
    except requests.exceptions.HTTPError as err:
        print("ERROR: Something went wrong retrieving the Github markdown", err)

    return content
