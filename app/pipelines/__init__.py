from flask import Blueprint

pipelines_bp = Blueprint('pipelines', __name__)

from app.pipelines import routes