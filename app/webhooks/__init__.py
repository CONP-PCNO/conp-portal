# -*- coding: utf-8 -*-
from flask import Blueprint
webhooks_bp = Blueprint('webhooks', __name__)
from app.webhooks import routes  # noqa: E402,F401
