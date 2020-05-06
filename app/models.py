# -*- coding: utf-8 -*-
"""Models Module

Module that contains the Data Models

"""
from app import db
from flask_user import UserMixin, user_registered
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.collections import attribute_mapped_collection
from datetime import datetime, timedelta
from pytz import timezone
import enum
from app.oauth import OAuth_pretty

eastern = timezone('US/Eastern')


class RoleMixin(object):
    """
    RoleMixin provides a method to set the default roles of a person
    at registration time.
    """
    @classmethod
    def before_commit(cls, session):
        for obj in list(session.new):
            if isinstance(obj, RoleMixin):
                obj.add_role("member")


db.event.listen(db.session, 'before_commit', RoleMixin.before_commit)


class User(db.Model, UserMixin, RoleMixin):
    """
        Provides User Model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User Authentication Information (Required by Flask-User)
    # we will use the users email as the primary means of login
    email = db.Column(db.String(128), unique=True)
    email_confirmed_at = db.Column(db.DateTime)
    password = db.Column(db.String(256), nullable=False, server_default='')
    active = db.Column(db.Boolean, nullable=False, server_default='0')

    # Customizable Fields
    full_name = db.Column(db.String(64), nullable=False, server_default='')
    affiliation = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow() + timedelta(days=365))
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    date_updated = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    # Many To One relationship
    affiliation_type_id = db.Column(
        db.Integer, db.ForeignKey('affiliation_type.id'))
    affiliation_type = db.relationship('AffiliationType')
    # One To Many relationship
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users'))

    def has_role(self, role):
        """
        Utility function to check if user has a particular role

        Args:
            role: role to test against

        Returns:
            True if the user has the role, otherwise, False
        """
        for item in self.roles:
            if item.name == role:
                return True
        return False

    def role(self):  # To DO: is this needed
        for item in self.roles:
            return item.name

    def add_role(self, role_name, add_to_roles=True):
        """
        Utility function that can add roles to users

        Args:
            role_name: name of the role to add
            add_to_roles: if True, it will add the role if it doesn't exist
                          if False, will only add if the role is there will return
                                    False if it cannot
        Result:
            True if the role has been added to the user
            False if the role cannot be added to the user
        """
        # check if the role exists
        if role_name is None:
            return False

        if self.has_role(role_name):
            return True

        rl = Role.query.filter(Role.name == role_name).first()

        if rl is None:
            if add_to_roles:
                rl = Role(name=role_name, label=role_name)
            else:
                return False
        self.roles.append(rl)
        return True

    def affiliation_type_key(self):
        """
        Utility function to return the key for the affilaition type
        """
        return self.affiliation_type.name

    def associated_oauths(self):
        """
        Utility function that returns the information about
        the oauths this user has associated with
        """
        oauths = OAuth.query.filter(OAuth.user == self).all()
        return [(x.provider, x.provider_user_login, OAuth_pretty[x.provider]) for x in oauths]

    def is_oauth_associated(self, provider_name):
        if OAuth.query.filter(OAuth.user == self,
                              OAuth.provider == provider_name).first():
            return True
        else:
            return False

    def __repr__(self):
        return '<User {}: {}>'.format(self.email, self.full_name)


class AffiliationType(db.Model):
    """
    Provides The Types of Affiliations that a user can select
    """
    __tablename__ = "affiliation_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False,
                     server_default='', unique=True)
    # for display purposes
    label = db.Column(db.String(255), server_default='')


class Role(db.Model):
    """
    Provides Role Model for Role based authorization
    """
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    # for @roles_accepted()
    name = db.Column(db.String(50), nullable=False,
                     server_default='', unique=True)
    # for display purposes
    label = db.Column(db.String(255), server_default='')

    def __repr__(self):
        return self.name


class UsersRoles(db.Model):
    """
    Provides a pivot table for user role association
    """
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


# OAUTH Model
class OAuth(OAuthConsumerMixin, db.Model):
    """
    provides a pivot table for oauth associations
    """
    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)
    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User,
                           backref=db.backref("oauth",
                                              collection_class=attribute_mapped_collection(
                                                  'provider'),
                                              cascade="all, delete-orphan")
                           )


class Dataset(db.Model):
    """
        Provides DataSet Model
    """
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.String(256), index=True, unique=True)
    description = db.Column(db.Text, index=True)
    name = db.Column(db.String(256), index=True)
    fspath = db.Column(db.Text)
    version = db.Column(db.String(6), index=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())
    is_private = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)


class Pipeline(db.Model):
    """
        Provides Pipeline Model for describing metadata for an execution pipeline
    """
    __tablename__ = 'pipelines'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, index=True, unique=True)
    owner_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(256), index=True)
    version = db.Column(db.String(128), index=True)
    is_private = db.Column(db.Boolean, index=True)
    date_created = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(tz=eastern))
    date_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now(tz=eastern))

    def __repr__(self):
        return '<Pipeline {}>'.format(self.name)
