# -*- coding: utf-8 -*-
from flask import Blueprint
profile_bp = Blueprint('profile', __name__)
from app.profile import routes  # noqa: E402,F401
