from flask import (
    current_app,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    session,
    make_response, 
    Response,
    abort
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

import os
import io
import zipfile

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
        "modalities": dats.experiment_modalities,
        "primarySoftware": dats.software_requirements,
        "primaryFunction": dats.function_assessed,
        "doi": "",
        "views": exp.views,
        "downloads": exp.downloads,
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
    
    # Mettre à jour le compteur de téléchargements
    # experiment.downloads = (experiment.downloads or 0) + 1

    # Chemin d'accès aux fichiers de l'expérimentation
    experiment_files_path = experiment.fspath

    print(experiment_files_path)
    # Créer un objet BytesIO pour stocker le fichier zip en mémoire
    # memory_file = io.BytesIO()

    # with zipfile.ZipFile(memory_file, 'w') as zf:
    #     # Vérifiez si le chemin est un dossier et non un fichier individuel
    #     if os.path.isdir(experiment_files_path):
    #         for root, dirs, files in os.walk(experiment_files_path):
    #             for file in files:
    #                 file_path = os.path.join(root, file)
    #                 zf.write(file_path, os.path.relpath(file_path, start=experiment_files_path))
    #     elif os.path.isfile(experiment_files_path):
    #         zf.write(experiment_files_path, os.path.basename(experiment_files_path))
    #     else:
    #         abort(404, description="Experiment files not found.")

    # # Repositionner le curseur du fichier au début
    # memory_file.seek(0)

    # db.session.commit()

    # return send_file(memory_file, mimetype='application/zip', as_attachment=True, attachment_filename='experiment.zip')

    # Vérifier si le fichier existe
    if not os.path.isdir(experiment_files_path):
        abort(404, description="File not found.")

    def generate():
        with open(experiment_files_path, "rb") as f:
            chunk = f.read(4096)
            while chunk:
                yield chunk
                chunk = f.read(4096)

        # Récupérer le nom du fichier pour le header
    filename = os.path.basename(experiment_files_path)

    return Response(generate(), mimetype="application/octet-stream", headers={"Content-Disposition": f"attachment;filename={filename}"})

@experiments_bp.route("/view/<int:experiment_id>")
def view(experiment_id):
    experiment = Experiment.query.filter(Experiment.id == experiment_id).first_or_404()
    readme_path = os.path.join(experiment.fspath, "README.md")
    readme_content = ""

    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r') as file:
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
    # if not request.cookies.get(cookie_name):
    #     # Si le cookie n'existe pas, incrémentez le compteur de vues et créez le cookie
    #     experiment.views = (experiment.views or 0) + 1
    #     db.session.commit()
    #     # Définir le cookie pour une période, par exemple 24 heures (86400 secondes)
    #     resp.set_cookie(cookie_name, 'true', max_age=86400)

    return resp


@experiments_bp.route("experiment_logo/<int:experiment_id>")
def get_experiment_logo(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)

    dats = DATSExperiment(experiment.fspath)
    with open(dats.LogoFilepath, 'rb') as logo_file:
        return logo_file.read()


@experiments_bp.route("/search")
# @experiments_bp.route("/search/", defaults={"keyword": None})
# @experiments_bp.route("/search/<string:keyword>")
def search():
    experiments = Experiment.query.all()
    experiment_dict = [
        experiment_as_dict(exp) for exp in experiments
    ]

    # Si le paramètre keyword est vide (chaîne vide), vous pouvez le traiter comme non spécifié.
    # if not keyword:
    #     return render_template("experiments/search.html", experiments=experiment_dict, keyword="")

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
