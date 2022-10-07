import itertools
import math
from flask import request, render_template, url_for, redirect, flash

from . import experiments_bp

from .data import data
from .forms import ExperimentForm, SearchForm
from .. import db
from ..models import Experiment




def get_unique_values(column) -> list:
    unique_values = [[y for y in x] for x in db.session.query(column).distinct()]
    unique_values = [x.split(',') for x in list(set(itertools.chain(*unique_values)))]
    unique_values = [x.strip() for x in list(set(itertools.chain(*unique_values)))]
    return unique_values

@experiments_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ExperimentForm()
    if form.validate_on_submit():
        flash('Done!')
        print(form.data)
        experiment = Experiment(**form.get_experiment_data())
        db.session.add(experiment)
        db.session.commit()
        return redirect(url_for('.submit'))
    return render_template('experiments/submit.html', data=data, form=form) 
