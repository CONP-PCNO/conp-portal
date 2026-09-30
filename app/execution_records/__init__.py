from flask import Blueprint

execution_records_bp = Blueprint('execution_records', __name__)
from app.execution_records import routes  # noqa: F401, E402
