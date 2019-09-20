# -*- coding: utf-8 -*-
"""
Defines forms needed for Flask-User login
"""
from flask_wtf import FlaskForm
from flask_user.forms import RegisterForm
from flask_user import UserManager
from wtforms import StringField, SelectField
from wtforms.widgets import ListWidget
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Required
from flask_user.forms import password_validator
from app import db
from app.models import Role, User, AffiliationType
from app.utils.form_utils import possible_affiliation_types


class CustomRegisterForm(RegisterForm):
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

    def validate_affiliation_type(form, field):
        """
        Needed or the validation bombs
        Not a big deal as it is set by a dropdown menu.
        """
        pass


class CustomUserManager(UserManager):
    """
    Custom User Manager for overriding Flask-User Forms
    """

    def customize(self, app):
        """
        Customizes classes for Flask-User
        """
        self.RegisterFormClass = CustomRegisterForm
