import os

from flask import (
    abort,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from .. import db
from ..models import Experiment
from . import experiments_bp
from .dats import DATSExperiment
from .experiment_page import FACETS, SORTS, experiment_card, experiment_page, filter_cards


def experiment_slug(exp: Experiment) -> str:
    """The stable part of an experiment's address: its folder name in
    conp-experiments ("projects/BADE-evidence-integration" ->
    "BADE-evidence-integration"). Database ids change when the table is
    rebuilt; this does not."""
    return (exp.experiment_id or str(exp.id)).split('/', 1)[-1]


def find_experiment(key):
    """An experiment by its address: the folder name, the full
    experiment_id ("projects/…") or, for old links, the numeric id."""
    key = str(key or '').strip().strip('/')
    if not key:
        return None
    if key.isdigit():
        return Experiment.query.filter(Experiment.id == int(key)).first()
    return Experiment.query.filter(
        Experiment.experiment_id.in_([key, 'projects/' + key])).first()


@experiments_bp.route("/")
@experiments_bp.route("/search")
def home():
    """The Experiments list: search box, filters and sort as plain GET
    parameters (q, function, modality, software, language, sort), so every
    view has its own address. "keyword" (old links) is read as q."""
    query = (request.args.get('q') or request.args.get('keyword') or '').strip()
    sort = request.args.get('sort', 'added')
    selected = {key: request.args.getlist(key) for key, _label, _field in FACETS}
    cards = [experiment_card(exp) for exp in Experiment.query.all()]
    shown, facets = filter_cards(cards, query, selected, sort)
    return render_template("experiments/search.html", cards=shown, total=len(cards), facets=facets,
                           query=query, sort=sort, sorts=SORTS,
                           filtered=bool(query or any(selected.values())))


@experiments_bp.route("/download/<int:experiment_id>")
def download(experiment_id):
    experiment = Experiment.query.filter(Experiment.id == experiment_id).first_or_404()

    # Mettre à jour le compteur de téléchargements
    experiment.downloads = (experiment.downloads or 0) + 1

    experiment_zip_path = experiment.fspath + ".zip"

    # Vérifier si le fichier ZIP existe
    if not os.path.exists(experiment_zip_path):
        abort(404, description="Experiment ZIP file not found.")

    db.session.commit()

    # Télécharger le fichier ZIP
    return send_file(experiment_zip_path, as_attachment=True, download_name=os.path.basename(experiment_zip_path))


@experiments_bp.route("/view/<path:key>")
def view(key):
    experiment = find_experiment(key)
    if experiment is None:
        abort(404)
    # Old numeric links (/experiments/view/1) move to the stable address.
    if key.strip('/') != experiment_slug(experiment):
        return redirect(url_for('experiments.view', key=experiment_slug(experiment)), code=301)
    experiment_id = experiment.id
    resp = make_response(render_template("experiments/experiment.html",
                                         page=experiment_page(experiment, _readme_html(experiment))))

    # Vérifiez si le cookie est déjà défini pour cet utilisateur et cette expérience spécifique
    cookie_name = f'viewed_exp_{experiment_id}'
    if not request.cookies.get(cookie_name):
        # Si le cookie n'existe pas, incrémentez le compteur de vues et créez le cookie
        experiment.views = (experiment.views or 0) + 1
        db.session.commit()
        # Définir le cookie pour une période, par exemple 24 heures (86400 secondes)
        resp.set_cookie(cookie_name, 'true', max_age=86400)

    return resp


@experiments_bp.route("experiment_logo/<int:experiment_id>")
def get_experiment_logo(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)

    dats = DATSExperiment(experiment.fspath)
    if not dats.LogoFilepath or not os.path.isfile(dats.LogoFilepath):
        abort(404)
    # send_file sets the image type from the file name (was sent as text/html)
    return send_file(dats.LogoFilepath)


@experiments_bp.route("/submit", methods=["GET", "POST"])
def submit():
    """Experiments are curated by hand for now: the old submission form
    (2022) wrote to columns the Experiment table no longer has and failed
    with an error. Experiment metadata is prepared in the DATS editor."""
    return redirect(url_for('main.dats_editor'), code=302)


def _readme_html(experiment):
    """The README rendered as on dataset pages (GitHub's Markdown API), with a
    first heading that repeats the title removed; '' when there is none."""
    from app.search.dataset_page import strip_title_heading
    from app.services import github
    path = os.path.join(experiment.fspath or '', 'README.md')
    if not os.path.isfile(path):
        return ''
    try:
        with open(path) as f:
            return strip_title_heading(github.render_content(f.read()), experiment.name)
    except Exception as e:  # GitHub unreachable: the page still renders
        print(e)
        return ''
