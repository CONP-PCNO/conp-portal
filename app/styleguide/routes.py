from flask import render_template
from flask_login import current_user

from app.styleguide import styleguide_bp

@styleguide_bp.route('/styleguide')

def styleguide():
    return render_template('styleguide.html', title='Styleguide | CONP')
