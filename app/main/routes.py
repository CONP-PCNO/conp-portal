from flask import render_template
from flask_login import current_user, login_required

from app.main import main_bp

@main_bp.route('/')
@main_bp.route('/public')
def public():
    return render_template('public.html', title='Home | CONP')

@main_bp.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='CONP | Home', user=current_user)