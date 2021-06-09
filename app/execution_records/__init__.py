# -*- coding: utf-8 -*-
from flask import Blueprint
execution_records_bp = Blueprint('execution_records', __name__)
from app.execution_records import routes  # noqa: E402,F401
