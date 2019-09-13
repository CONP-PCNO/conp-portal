from flask import Blueprint

styleguide_bp = Blueprint('styleguide', __name__)

from app.styleguide import routes
