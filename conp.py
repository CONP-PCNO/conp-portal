# -*- coding: utf-8 -*-
"""
Main module that will call and create the flask app
"""
from app import create_app, db, cli
from app.models import Dataset, Pipeline

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """
    Makes sure there is a shell context for running flask shell
    """
    return {
        'db': db,
        'Dataset': Dataset,
        'Pipeline': Pipeline
    }
