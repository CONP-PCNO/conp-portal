from flask import render_template

from app.styleguide import styleguide_bp


@styleguide_bp.route('/styleguide')
def styleguide():
    return render_template('styleguide.html', title='Styleguide | CONP')
