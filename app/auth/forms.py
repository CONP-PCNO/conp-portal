# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_user.forms import RegisterForm
from flask_user import UserManager
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Required, ValidationError
from flask_user.forms import password_validator
from app import db
from app.models import Role


class RoleMultiField(SelectMultipleField):
    def pre_validation(self, form):
        pass


class CustomRegisterForm(RegisterForm):
    affiliation = StringField('Affiliation',
                              validators=[DataRequired('Please enter the insitution'
                                                       ' with which you are affiated')])
    roles = RoleMultiField('Roles',
                           widget=ListWidget(prefix_label=True))

    def validate_roles(form, field):
        if field.data is None or len(field.data) == 0:
            raise ValidationError("Need to specify at least one role for the user")


class CustomUserManager(UserManager):
  def customize(self, app):
    self.RegisterFormClass = CustomRegisterForm

