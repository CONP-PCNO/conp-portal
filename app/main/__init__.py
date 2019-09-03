from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.main import routes