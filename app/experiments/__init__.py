from flask import Blueprint

experiments_bp = Blueprint('experiments', __name__, url_prefix='/experiments')
from . import routes  # noqa: F401, E402
