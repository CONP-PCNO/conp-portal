""" Routes Module

    Currently this module contains all of the routes for the main blueprint
"""
import glob
import json
import os
from urllib.parse import urlencode, urlparse

from flask import abort, current_app, redirect, render_template
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

    # Headline counts for the hero strip. Best-effort: the homepage must
    # never fail because a count could not be computed (e.g. the Boutiques
    # cache is absent in a fresh dev environment).
    counts = None
    try:
        count_datasets = Dataset.query.count()

        cache_dir = os.path.join(
            os.path.expanduser('~'), ".cache", "boutiques", "production")
        with open(os.path.join(cache_dir, "all_descriptors.json"), "r") as f:
            all_descriptors = json.load(f)
        with open(os.path.join(cache_dir, "detailed_all_descriptors.json"), "r") as f:
            detailed_all_descriptors = json.load(f)
        # Same rule as the Tools page: skip deprecated and blocked tools.
        with open(os.path.join(os.getcwd(), "app/static/pipelines/block-list-pipeline.json")) as f:
            blocked = set(json.load(f))
        count_pipelines = len([
            d_index
            for d_index, descriptor in enumerate(all_descriptors)
            if not detailed_all_descriptors[d_index].get("DEPRECATED", False)
            and {**descriptor, **detailed_all_descriptors[d_index]}.get("ID") not in blocked
        ])

        counts = {"datasets": count_datasets, "pipelines": count_pipelines}
    except Exception:
        current_app.logger.warning(
            "Could not compute homepage counts", exc_info=True)

    return render_template('index.html', title='CONP | Home', user=current_user,
                           counts=counts)


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


@main_bp.route('/download')
def download():
    """ Download Route

        Route to lead to the download page

        Args:
            None

        Returns:
            rendered template for download.html
    """

    content = github.get_download_content()

    return render_template('download.html', title='CONP | Download a Dataset', user=current_user, content=content)


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


@main_bp.route('/data-governance')
def data_governance():
    """ Data Governance Route

        Route to lead to the data governance page

        Args:
            None

        Returns:
            rendered template for data_governance.html
    """

    content = github.get_data_governance_content()

    return render_template('data_governance.html', title='CONP | Data Governance', user=current_user, content=content)


CONTACT_FORM = ('https://docs.google.com/forms/d/e/'
                '1FAIpQLSe01Po0tXd11JDzYF9Jtfpj1eReiSPDXCEknpxK_6NEGL6D2A/viewform')
# The Google Form branches on "Nature of your feedback?" (entry 1130948154); each
# branch ends in its own message box. topic= picks the branch, message= starts the text.
CONTACT_TOPICS = {
    'bug': ('Problem or bug report', 1130875829),
    'ux': ('Suggestions or comments regarding user experience', 702605877),
    'suggestion': ('Feature, dataset, or pipeline suggestion', 694294914),
    'other': ('Other topic or general feedback', 470057101),
}


def contact_form_src(topic=None, message=None):
    """The embedded form's address, pre-filled when topic (and message) are given."""
    params = [('embedded', 'true')]
    if topic in CONTACT_TOPICS:
        label, message_entry = CONTACT_TOPICS[topic]
        params += [('usp', 'pp_url'), ('entry.1130948154', label)]
        if message:
            params.append((f'entry.{message_entry}', message.strip()[:500]))
    return CONTACT_FORM + '?' + urlencode(params)


@main_bp.route('/contact_us')
def contact_us():
    """ Contact Us Route

        Route to lead to the contact page. Optional query parameters pre-fill the
        form: topic (bug, ux, suggestion, other) and message, e.g. a dataset page's
        "Tell us about a paper we missed" link:
        /contact_us?topic=other&message=A paper that used "<title>" is missing...

        Args:
            None

        Returns:
            rendered template for contact_us.html
    """

    form_src = contact_form_src(flask_request.args.get('topic'), flask_request.args.get('message'))
    return render_template('contact_us.html', title='CONP | Contact Us', user=current_user, form_src=form_src)


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
    # @todo: remove hard-coded path and the need to read from the cache. Instead query the database for the number of pipelines.
    cache_dir = os.path.join(os.path.expanduser(
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")

    with open(all_desc_path) as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path) as f:
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

    # The conp-react build names its stylesheet with a content hash
    # (main.<hash>.css) that changes on every rebuild. Look it up instead of
    # hard-coding it: a stale name 404s and the editor's last step (the
    # README editor) renders unstyled.
    css_dir = os.path.join(current_app.static_folder, 'lib', 'conp-react', 'umd')
    css_files = sorted(glob.glob(os.path.join(css_dir, 'main.*.css')), key=os.path.getmtime)
    editor_css = 'lib/conp-react/umd/' + os.path.basename(css_files[-1]) if css_files else None

    return render_template('dats-editor.html', title='CONP | Metadata Editor', user=current_user,
                           editor_css=editor_css)


@main_bp.route('/ark:/<url_naan>/<url_ark_id>')
def redirect_ark_ids(url_naan, url_ark_id):

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

    # An ARK we never minted is "not found" (it was a server error: the
    # lookup's empty result was indexed). A retired dataset's ARK still
    # redirects: /dataset shows its "retired" page.
    if url_ark_id.startswith('d7'):
        db_entry = db.session.query(ArkId.dataset_id).filter_by(
            ark_id=requested_full_ark_id
        ).first()
        if db_entry and db_entry[0]:
            redirect_url = f'/dataset?id={db_entry[0]}'
    elif url_ark_id.startswith('p7'):
        db_entry = db.session.query(ArkId.pipeline_id).filter_by(
            ark_id=requested_full_ark_id
        ).first()
        if db_entry and db_entry[0]:
            redirect_url = f'/pipeline?id={db_entry[0]}'
    elif url_ark_id.startswith('e7'):
        # Experiments (the minter has an "e7" shoulder; none are minted yet).
        db_entry = db.session.query(ArkId.experiment_id).filter_by(
            ark_id=requested_full_ark_id
        ).first()
        if db_entry and db_entry[0]:
            folder = str(db_entry[0]).split('/', 1)[-1] if str(db_entry[0]).startswith('projects/') else db_entry[0]
            redirect_url = f'/experiments/view/{folder}'

    if not redirect_url:
        abort(
            404,
            f'The provided ARK ID {requested_full_ark_id} does not match any '
            f' dataset, pipeline or experiment from the CONP portal. Please verify the URL.'
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
