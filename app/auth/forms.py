# -*- coding: utf-8 -*-
"""
Defines forms needed for Flask-User login
"""
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from app.utils.form_utils import possible_affiliation_types


class CustomRegisterForm():
    """
    Custom Form Class to define custom members of the User Model
    """
    full_name = StringField('Full Name', validators=[
                            DataRequired('Please enter your full name')])

    affiliation = StringField('Affiliation',
                              validators=[DataRequired('Please enter the insitution'
                                                       ' with which you are affiated')])
    agreeToTerms = BooleanField('I Agree to the CONP Terms and Conditions',
                                validators=[DataRequired('Need to agree to the terms to register account')])

    def validate_affiliation_type(form, field):
        """
        Needed or the validation bombs
        Not a big deal as it is set by a dropdown menu.
        """
        pass


class CustomUserManager():
    """
    Custom User Manager for overriding Flask-User Forms
    """

    def customize(self, app):
        """
        Customizes classes for Flask-User
        """
        self.RegisterFormClass = CustomRegisterForm
