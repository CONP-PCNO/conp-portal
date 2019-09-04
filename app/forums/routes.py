from flask import render_template
from flask_login import current_user

from app.forums import forums_bp

@forums_bp.route('/forums')
def forums():
    return render_template('forums.html', title='CONP | Forums', user=current_user)