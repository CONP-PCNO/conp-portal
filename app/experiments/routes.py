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
from sqlalchemy import inspect

from .. import db
from ..models import Experiment
from . import experiments_bp
from .dats import DATSExperiment


def to_camel_case(snake_str: str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def object_as_dict(obj: object):
    return {to_camel_case(c.key): getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


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


def experiment_as_dict(exp: Experiment):
    dats = DATSExperiment(exp.fspath)
    return {
        "slug": experiment_slug(exp),
        "pageUrl": url_for('experiments.view', key=experiment_slug(exp)),
        "title": exp.name,
        "description": dats.description,
        "creators": dats.creators,
        "version": dats.version,
        "dateAdded": exp.date_added_to_portal,
        "dateUpdated": exp.date_updated,
        "license": dats.licenses,
        "modalities": dats.experiment_modalities,
        "primarySoftware": dats.software_requirements,
        "primaryFunction": dats.function_assessed,
        "primaryPublications": dats.primaryPublications,
        "doi": "",
        "views": exp.views,
        "downloads": exp.downloads,
        "imageFile": dats.LogoFilepath,
        "repositoryFileCount": dats.fileCount,
        "repositorySize": dats.size,
        "repositoryFile": dats.DatsFilepath,
        "id": exp.id,
        "origin": dats.origin,
        "contactPerson": dats.contacts if dats.contacts else None,
        "contactEmail": dats.contacts if dats.contacts else None,
        "privacy": dats.privacy,
        "keywords": ", ".join(dats.keywords),
        "otherSoftware": dats.software_requirements,
        "otherFunctions": dats.function_assessed,
        "acknowledgements": dats.acknowledges,
        "source": dats.sources,
        "remoteUrl": exp.remoteUrl
    }


@experiments_bp.route("/")
def home():
    # Récupérer le paramètre 'keyword' de l'URL, sinon None par défaut
    keyword = request.args.get('keyword')
    experiments = Experiment.query.all()
    experiment_dict = [
        experiment_as_dict(exp) for exp in experiments
    ]

    # Si le paramètre keyword est vide (chaîne vide), vous pouvez le traiter comme non spécifié.
    if not keyword:
        return render_template("experiments/search.html", experiments=experiment_dict, keyword="")

    return render_template("experiments/search.html", experiments=experiment_dict, keyword=keyword)


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
    readme_path = os.path.join(experiment.fspath, "README.md")
    readme_content = ""

    if os.path.exists(readme_path):
        try:
            with open(readme_path) as file:
                readme_content = file.read()
        except Exception as e:
            print(e)  # Il est préférable de loguer l'exception plutôt que de passer silencieusement

    readme_md = readme_content

    # Préparez la réponse et rendez le template
    resp = make_response(render_template("experiments/experiment.html",
                                         experiment=experiment_as_dict(experiment),
                                         readme=readme_md))

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


@experiments_bp.route("/search")
def search():
    # Récupérer le paramètre 'keyword' de l'URL, sinon None par défaut
    keyword = request.args.get('keyword')
    experiments = Experiment.query.all()
    experiment_dict = [
        experiment_as_dict(exp) for exp in experiments
    ]

    # Si le paramètre keyword est vide (chaîne vide), vous pouvez le traiter comme non spécifié.
    if not keyword:
        return render_template("experiments/search.html", experiments=experiment_dict, keyword="")

    return render_template("experiments/search.html", experiments=experiment_dict, keyword=keyword)


@experiments_bp.route("/submit", methods=["GET", "POST"])
def submit():
    """Experiments are curated by hand for now: the old submission form
    (2022) wrote to columns the Experiment table no longer has and failed
    with an error. Experiment metadata is prepared in the DATS editor."""
    return redirect(url_for('main.dats_editor'), code=302)
