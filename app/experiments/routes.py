from flask import (
    current_app,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    session,
    abort,
    send_file
)

from sqlalchemy import inspect

from . import experiments_bp
from .data import data
from .filters import get_filters
from .forms import ExperimentForm
from .dats import DATSExperiment
from .search import SearchEngine
from .sort import SortKey
from .utils import upload_file
from .. import config, db
from ..models import Experiment

def to_camel_case(snake_str: str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def object_as_dict(obj: object):
    return {to_camel_case(c.key): getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def experiment_as_dict(exp: Experiment):
    dats = DATSExperiment(exp.fspath)
    return {
        "title": exp.name,
        "description": dats.description,
        "creators": dats.creators,
        "version": dats.version,
        "dateAdded": exp.date_added_to_portal,
        "dateUpdated": exp.date_updated,
        "license": dats.licenses,
        "modalities": dats.modalities,
        "primarySoftware": dats.software_requirements,
        "primaryFunction": dats.function_assessed,
        "doi": "",
        "views": "",
        "downloads": "",
        "imageFile": dats.LogoFilepath,
        "repositoryFileCount": dats.fileCount,
        "repositorySize": dats.size,
        "id": exp.id,
        "origin": dats.origin,
        "contactPerson": dats.contacts if dats.contacts else None,
        "contactEmail": dats.contacts if dats.contacts else None,
        "privacy": dats.privacy,
        "keywords": ", ".join(dats.keywords),
        "otherSoftware": dats.software_requirements,
        "otherFunctions": dats.function_assessed,
        "acknowledgements": dats.acknowledges,
        "source": dats.sources
    }

@experiments_bp.route("/")
def home():
    return render_template("experiments/home.html")

@experiments_bp.route("/download/<int:experiment_id>")
def download(experiment_id):
    experiment = Experiment.query.filter(Experiment.id == experiment_id).first_or_404()
    experiment.increment_downloads()
    return send_file(experiment.repository_file, mimetype='application/zip', as_attachment=True, attachment_filename='experiment')

@experiments_bp.route("/view/<int:experiment_id>")
def view(experiment_id):
    experiment = Experiment.query.filter(Experiment.id == experiment_id).first_or_404()
    return render_template(
        "experiments/experiment.html",
        experiment=experiment_as_dict(experiment)
    )


@experiments_bp.route("experiment_logo/<int:experiment_id>")
def get_experiment_logo(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)

    dats = DATSExperiment(experiment.fspath)
    with open(dats.LogoFilepath, 'rb') as logo_file:
        return logo_file.read()


@experiments_bp.route("/search")
def search():
    experiments = Experiment.query.all()
    experiment_dict = [
        experiment_as_dict(exp) for exp in experiments
    ]

    return render_template("experiments/search.html", experiments=experiment_dict)


@experiments_bp.route("/submit", methods=["GET", "POST"])
def submit():
    form = ExperimentForm()

    if request.files and request.files.get("repository"):
        session["repository_file"] = upload_file(request.files.get("repository"))
    elif request.files and request.files.get("image_file"):
        session["image_file"] = upload_file(request.files.get("image_file"))

    if form.validate_on_submit():
        try:
            repository_file = session["repository_file"]
        except KeyError:
            flash("Uploading a repository is required!")
            return redirect(url_for(".submit"))
        try:
            image_file = session["image_file"]
        except KeyError:
            image_file = None

        flash("Done!")

        form.license.data = form.license.data.replace(' (Recommended)', '')

        params = {
            "title": form.title.data or None,
            "description": form.description.data or None,
            "creators": form.creators.data or None,
            "origin": form.origin.data or None,
            "contact_person": form.contact_person.data or None,
            "contact_email": form.contact_email.data or None,
            "version": form.version.data or None,
            "license": form.license.data or None,
            "keywords": form.keywords.data or None,
            "modalities": form.modalities.data or None,
            "primary_software": form.primary_software.data or None,
            "other_software": form.other_software.data or None,
            "primary_function": form.primary_function.data or None,
            "other_functions": form.other_functions.data or None,
            "doi": form.doi.data or None,
            "acknowledgements": form.acknowledgements.data or None,
            "repository_file": repository_file or None,
            "image_file": image_file or None
        }

        experiment = Experiment(**params)
        db.session.add(experiment)
        db.session.commit()
        return redirect(url_for(".submit"))

    return render_template("experiments/submit.html", data=data, form=form)


@experiments_bp.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(current_app.config["EXPERIMENTS_UPLOAD_DIRECTORY"], name)
