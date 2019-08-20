from flask import Blueprint

forums_bp = Blueprint('forums', __name__)

from app.forums import routes