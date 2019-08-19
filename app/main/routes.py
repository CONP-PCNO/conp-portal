from flask import render_template

from app.main import main_bp

@main_bp.route('/')
@main_bp.route('/public')
def public():
    return render_template('public.html', title='Home | CONP')