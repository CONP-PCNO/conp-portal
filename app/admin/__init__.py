# -*- coding: utf-8 -*-
from flask import Blueprint
admin_bp = Blueprint('admin', __name__)
from app.admin import routes  # noqa: E402,F401
