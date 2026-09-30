from flask import Blueprint

webhooks_bp = Blueprint('webhooks', __name__)
from app.webhooks import routes  # noqa: F401, E402
