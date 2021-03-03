# -*- coding: utf-8 -*-
"""
Contains the forms for User Profiles
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import ListWidget
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError
from app.utils.form_utils import possible_affiliation_types, RoleMultiField


class UserProfileForm(FlaskForm):
    """
    Form Class to be used for user profiles
    """
    full_name = StringField("Full Name", validators=[
                            DataRequired('Please give us your full name')])
    affiliation = StringField('Affiliation',
                              validators=[DataRequired('Please enter the insitution'
                                                       ' with which you are affiated')])
    affiliation_type = QuerySelectField('Current Status',
                                        query_factory=possible_affiliation_types,
                                        get_label='label', allow_blank=False)

    roles = RoleMultiField('Roles',
                           widget=ListWidget(prefix_label=True))

    def validate_roles(form, field):
        if field.data is None or len(field.data) == 0:
            raise ValidationError(
                "Need to specify at least one role for the user")

    def validate_affiliation_type(form, field):
        pass
