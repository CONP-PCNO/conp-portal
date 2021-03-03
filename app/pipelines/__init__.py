# -*- coding: utf-8 -*-
from flask import Blueprint
pipelines_bp = Blueprint('pipelines', __name__)
from app.pipelines import routes  # noqa: E402,F401
