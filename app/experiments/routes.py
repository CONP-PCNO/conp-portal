import itertools
import math
from flask import request, render_template, url_for, redirect, flash

from . import experiments_bp

from .data import data
from .forms import ExperimentForm
from .. import db
from ..models import Experiment

sort_key_options = {
    "Title (A-Z)": Experiment.title,
    "Title (Z-A)": Experiment.title.desc(),
}


def get_unique_values(column) -> list:
    unique_values = [[y for y in x] for x in db.session.query(column).distinct()]
    unique_values = [x.split(',') for x in list(set(itertools.chain(*unique_values)))]
    unique_values = [x.strip() for x in list(set(itertools.chain(*unique_values)))]
    return unique_values


@experiments_bp.route('/', methods=['GET'])
def home():
    return render_template('experiments/home.html')


@experiments_bp.route('/search')
def search():

    filters = {
        'modalities': {
            'options': get_unique_values(Experiment.modalities),
            'column': Experiment.modalities
        },
        'purpose': {
            'options': get_unique_values(Experiment.primary_function),
            'column': Experiment.primary_function
        },
        'software': {
            'options': get_unique_values(Experiment.primary_software),
            'column': Experiment.primary_software
        }
    }

    page = request.args.get('page', 1, int)
    per_page = request.args.get('per_page', 10, int)
    sort_key = request.args.get('sort_key', 'Title (A-Z)', str)
    filter_column = request.args.get('filter_column', None, str)
    filter_option = request.args.get('filter_option', None, str)


    try:
        query = Experiment.query.filter(filters[filter_column]['column'] == filter_option)
    except KeyError:
        query = Experiment.query

    # query = Experiment.query.order_by(sort_key_options.get(sort_key))
    pagination = query.order_by(sort_key_options.get(sort_key)).paginate(page=page, per_page=per_page)
    return render_template('experiments/search.html', pagination=pagination, math=math,
                           sort_key_options=sort_key_options, sort_key=sort_key, filters=filters)


@experiments_bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ExperimentForm()
    print(form.data)
    form.validate()
    if form.validate_on_submit():
        flash('Done!')
        print(form.data)
        experiment = Experiment(**form.get_experiment_data())
        db.session.add(experiment)
        db.session.commit()
        return redirect(url_for('.submit'))
    return render_template('experiments/submit.html', data=data, form=form)
