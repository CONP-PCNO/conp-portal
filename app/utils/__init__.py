from flask import Blueprint

utils_bp = Blueprint('utils', __name__)
from app.utils import form_utils  # noqa: F401, E402
