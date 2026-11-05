"""
Defines the registration form used by Flask-Security.
"""
from flask_security import RegisterFormV2
from wtforms import BooleanField, StringField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from app.utils.form_utils import possible_affiliation_types


class CustomRegisterForm(RegisterFormV2):
    """
    Custom Form Class to define custom members of the User Model
    """
    full_name = StringField('Full Name', validators=[
                            DataRequired('Please enter your full name')])

    affiliation = StringField('Affiliation',
                              validators=[DataRequired('Please enter the insitution'
                                                       ' with which you are affiated')])
    affiliation_type = QuerySelectField('Current Status',
                                        query_factory=possible_affiliation_types,
                                        get_label='label', allow_blank=False)

    agreeToTerms = BooleanField('I Agree to the CONP Terms and Conditions',
                                validators=[DataRequired('Need to agree to the terms to register account')])
