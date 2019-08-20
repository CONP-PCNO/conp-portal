from flask import render_template
from flask_login import current_user

from app.profile import profile_bp

@profile_bp.route('/profile')
def profile():
    return render_template('profile.html', title='CONP | My Profile', user=current_user)