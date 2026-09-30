from flask import Blueprint

search_bp = Blueprint('search', __name__)
from app.search import routes  # noqa: F401, E402
