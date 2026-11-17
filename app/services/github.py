import os

import requests


def render_content(raw):
    url = 'https://api.github.com/markdown'
    body = {
        "text": raw,
        "mode": "gfm",
        "context": "CONP-PCNO/conp-documentation"
    }

    headers = {}
    # Fallback to standard GITHUB_TOKEN if used in GitHub Actions, or GITHUB_PAT
    github_pat = os.environ.get('GITHUB_PAT') or os.environ.get('GITHUB_TOKEN')
    if github_pat:
        headers['Authorization'] = f'Bearer {github_pat}'

    response = requests.post(url, json=body, headers=headers)

    content = response.text.replace('user-content-', '')
    return content


def get_share_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/Share_Instruction_Page.md'
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
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/CONP_download.md'
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


def get_data_governance_content():
    content = None
    try:
        url = 'https://raw.githubusercontent.com/CONP-PCNO/conp-documentation/master/Documentation_displayed_on_the_portal/CONP_data_governance.md'
        headers = {'Content-type': 'text/html; charset=UTF-8'}
        response = requests.get(url, headers=headers)

        raw = response.text

        content = render_content(raw)
    except requests.exceptions.HTTPError as err:
        print("ERROR: Something went wrong retrieving the Github markdown", err)

    return content
