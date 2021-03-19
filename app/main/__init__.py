# -*- coding: utf-8 -*-
from flask import Blueprint
main_bp = Blueprint('main', __name__)
from app.main import routes  # noqa: E402,F401
