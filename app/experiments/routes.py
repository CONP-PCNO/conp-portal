from __future__ import annotations

from flask import flash, render_template, request, redirect, url_for

from . import experiments_bp
from .data import data
from .filters import get_filters
from .forms import ExperimentForm
from .search import SearchEngine
from .sort import SortKey
from .. import db
from ..models import Experiment

@experiments_bp.route('/')
def home():
  return render_template('experiments/home.html')

@experiments_bp.route('/search')
def search():
  filters = get_filters(request)
  page = request.args.get('page', 1, int)
  per_page = request.args.get('per_page', 10, int)
  search_term = request.args.get('search_term', None, str)
  sort_key = SortKey(request.args.get('sort_key', 'title_asc', str))
  
  query = Experiment.query
  for filter in filters:
    for option, active in filters[filter]['options'].items():
      if active:
        query = query.filter(getattr(Experiment, filter) == option)
  query = query.order_by(sort_key.column())

  if search_term:
    search_engine = SearchEngine()
    matching_ids = search_engine.search(search_term, query.all())
    query = query.filter(Experiment.id.in_(matching_ids))

  pagination = query.paginate(page=page, per_page=per_page)
  
  return render_template(
    'experiments/search.html', 
    filters=filters,
    pagination=pagination,
    sort_key=sort_key
  )

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
