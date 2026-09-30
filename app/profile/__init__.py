from flask import Blueprint

profile_bp = Blueprint('profile', __name__)
from app.profile import routes  # noqa: F401, E402
