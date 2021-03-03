# -*- coding: utf-8 -*-
from flask import Blueprint
analytics_bp = Blueprint('analytics', __name__)
from app.analytics import routes  # noqa: E402,F401
