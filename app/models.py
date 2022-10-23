# -*- coding: utf-8 -*-
"""Models Module

Module that contains the Data Models

"""

from __future__ import annotations

from app import db
from flask_user import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.collections import attribute_mapped_collection
from datetime import datetime, timedelta
from pytz import timezone
from app.oauth import OAuth_pretty
from random import randrange

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
    description = db.Column(db.Text)
    name = db.Column(db.String(256), index=True)
    fspath = db.Column(db.Text)
    remoteUrl = db.Column(db.Text)
    version = db.Column(db.String(6), index=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())
    date_added_to_portal = db.Column(db.DateTime, default=datetime.now())
    is_private = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)


class DatasetAncestry(db.Model):
    """
        Provides DatasetAncestry Model
    """
    __tablename__ = 'dataset_ancestry'

    id = db.Column(db.String(36), primary_key=True, unique=True)
    parent_dataset_id = db.Column(db.String(256), index=True)
    child_dataset_id = db.Column(db.String(256), index=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())

    __table_args__ = (db.UniqueConstraint(
        'parent_dataset_id', 'child_dataset_id', name='uix_1'),)

    def __repr__(self):
        return '<DatasetAncestry {}>'.format(self.id)


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


class MatomoDailyVisitsSummary(db.Model):
    """
    Provides Matomo Daily VisitsSummary Model to store Daily VisitsSummary

    avg_time_on_site     = average time spent, in seconds, on this page
    bounce_count         = number of visits that bounced (viewed only one page)
    max_actions          = maximum number of actions in a visit
    nb_actions           = number of actions (page views, outlinks and downloads)
    nb_uniq_visitors     = number of unique visitors
    nb_users             = number of unique active users (visitors with a known User ID).
                           If you are not using User ID then this metric will be set to zero.
    nb_visits            = number of visits (30 min of inactivity considered a new visit)
    nb_visits_converted  = number of visits that converted a goal
    sum_visit_length     = total time spent, in seconds
    """
    __tablename__ = 'matomo_daily_visits_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(12), unique=True)
    avg_time_on_site = db.Column(db.Integer)
    bounce_count = db.Column(db.Integer)
    max_actions = db.Column(db.Integer)
    nb_actions = db.Column(db.Integer)
    nb_actions_per_visit = db.Column(db.Float)
    nb_uniq_visitors = db.Column(db.Integer)
    nb_users = db.Column(db.Integer)
    nb_visits = db.Column(db.Integer)
    nb_visits_converted = db.Column(db.Integer)
    sum_visit_length = db.Column(db.Integer)

    def __repr__(self):
        return '<MatomoDailyVisitsSummary {}>'.format(self.id)


class MatomoDailyGetPageUrlsSummary(db.Model):
    """
    Provides Matomo Daily getPageUrls Model to store daily Visited Page Urls
    from the Matomo Actions.getPageUrls API endpoint.

    This will get the URLs for all pages except for the dataset specific
    pages. This will be stored in matomo_daily_dataset_views_summary.

    Chosen variables from the endpoint are:
    - url              = page URL
    - label            = page label
    - nb_hits          = number of views on this page
    - nb_visits        = number of visits (30 min of inactivity considered a new visit)
    - nb_uniq_visitors = number of unique visitors
    - sum_time_spent   = total time spent on this page, in seconds
    - avg_time_on_page = average time spent, in seconds, on this page
    """
    __tablename__ = 'matomo_daily_get_page_urls_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(12))
    url = db.Column(db.Text)
    label = db.Column(db.String(256))
    nb_hits = db.Column(db.Integer)
    nb_visits = db.Column(db.Integer)
    nb_uniq_visitors = db.Column(db.Integer)
    sum_time_spent = db.Column(db.Integer)
    avg_time_on_page = db.Column(db.Float)

    def __repr__(self):
        return '<MatomoDailyGetPageUrlsSummary {}>'.format(self.id)


class MatomoDailyGetDatasetPageViewsSummary(db.Model):
    """
    Provides Matomo daily dataset views summary to store the statistics
    on the different dataset pages that could not be stored in
    matomo_daily_get_page_urls_summary.

    Chosen variables from the endpoint are:
    - url              = page URL
    - label            = page label
    - nb_hits          = number of views on this page
    - nb_visits        = number of visits (30 min of inactivity considered a new visit)
    - nb_uniq_visitors = number of unique visitors
    - sum_time_spent   = total time spent on this page, in seconds
    - avg_time_on_page = average time spent, in seconds, on this page
    """
    __tablename__ = 'matomo_daily_dataset_page_views_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataset_id = db.Column(db.String(256))
    date = db.Column(db.String(12))
    url = db.Column(db.Text)
    label = db.Column(db.String(256))
    nb_hits = db.Column(db.Integer)
    nb_visits = db.Column(db.Integer)
    nb_uniq_visitors = db.Column(db.Integer)
    sum_time_spent = db.Column(db.Integer)
    avg_time_on_page = db.Column(db.Float)

    def __repr__(self):
        return '<MatomoDailyGetDatasetPageViewsSummary {}>'.format(self.id)


class MatomoDailyGetPortalDownloadSummary(db.Model):
    """
    Provides Matomo daily download summary to store the statistics
    on the different downloads via the portal.

    Chosen variables from the endpoint are:
    - url              = page URL
    - label            = page label
    - nb_hits          = number of views on this page
    - nb_visits        = number of visits (30 min of inactivity considered a new visit)
    - nb_uniq_visitors = number of unique visitors
    - sum_time_spent   = total time spent on this page, in seconds
    - segment          = segment with download URL
    """
    __tablename__ = 'matomo_daily_portal_download_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(12))
    url = db.Column(db.Text)
    label = db.Column(db.String(256))
    nb_hits = db.Column(db.Integer)
    nb_visits = db.Column(db.Integer)
    nb_uniq_visitors = db.Column(db.Integer)
    sum_time_spent = db.Column(db.Integer)
    segment = db.Column(db.String(256))

    def __repr__(self):
        return '<MatomoDailyGetPortalDownloadSummary {}>'.format(self.id)


class MatomoDailyGetSiteSearchKeywords(db.Model):
    """
    Provides Matomo daily site search keywords statistics to store
    the search keyword statistics in matomo_daily_site_keyword_searches_summary

    avg_time_on_page    = average time spent, in seconds, on this page
    bounce_rate         = ratio of visits leaving the website after landing on this page
    exit_nb_visits      = number of visits that finished on this page
    exit_rate           = ratio of visits that do not view any other page after this page
    label               = keyword searched
    nb_hits             = number of views on this page
    nb_pages_per_search = number of pages displayed for the searched keyword
    nb_visits           = number of visits (30 min of inactivity considered a new visit)
    segment             = segment with keyword search
    sum_time_spent      = total time spent on this page, in seconds
    """

    __tablename__ = 'matomo_daily_site_keyword_searches_summary'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(12))
    avg_time_on_page = db.Column(db.Integer)
    bounce_rate = db.Column(db.String(64))
    exit_nb_visits = db.Column(db.Integer)
    exit_rate = db.Column(db.String(64))
    label = db.Column(db.String(256))
    nb_hits = db.Column(db.Integer)
    nb_pages_per_search = db.Column(db.Integer)
    nb_visits = db.Column(db.Integer)
    segment = db.Column(db.Text)
    sum_time_spent = db.Column(db.Integer)

    def __repr__(self):
        return '<MatomoDailyGetSiteSearchKeywords {}>'.format(self.id)


class ArkId(db.Model):

    __tablename__ = 'ark_id'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ark_id = db.Column(db.String(128), unique=True)
    dataset_id = db.Column(db.String(256))
    pipeline_id = db.Column(db.String(64))

    def __repr__(self):
        return '<ArkId {}>'.format(self.id)


class GithubDailyClonesCount(db.Model):
    """
    Provides GitHub daily clones' count to be stored in database table
    github_daily_clones_count.

    repo         = name of the GitHub repository
    date         = date associated to the count
    timestamp    = timestamp associated to the count
    count        = number of clones of the GitHub repository for a given date
    unique_count = number of unique clones for a given date
    """

    __tablename__ = "github_daily_clones_count"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo = db.Column(db.String(256))
    date = db.Column(db.String(12))
    timestamp = db.Column(db.String(30))
    count = db.Column(db.Integer)
    unique_count = db.Column(db.Integer)

    def __repr__(self):
        return '<GithubDailyClonesCount {}>'.format(self.id)


class GithubDailyViewsCount(db.Model):
    """
    Provides GitHub daily views' count to be stored in database table
    github_daily_views_count.

    repo         = name of the GitHub repository
    date         = date associated to the count
    timestamp    = timestamp associated to the count
    count        = number of views of the GitHub repository for a given date
    unique_count = number of unique views for a given date
    """

    __tablename__ = "github_daily_views_count"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo = db.Column(db.String(256))
    date = db.Column(db.String(12))
    timestamp = db.Column(db.String(30))
    count = db.Column(db.Integer)
    unique_count = db.Column(db.Integer)

    def __repr__(self):
        return '<GithubDailyViewsCount {}>'.format(self.id)

## Experiments ##


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    creators = db.Column(db.PickleType)
    origin = db.Column(db.Text, default='NA')
    contact_person = db.Column(db.Text)
    contact_email = db.Column(db.Text)
    version = db.Column(db.Float, default=-1.0)
    date_added = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())
    privacy = db.Column(db.Text)
    license = db.Column(db.Text, default='NA')
    keywords = db.Column(db.PickleType)
    modalities = db.Column(db.PickleType)
    primary_software = db.Column(db.Text)
    other_software = db.Column(db.PickleType, default=[])
    primary_function = db.Column(db.Text)
    other_functions = db.Column(db.PickleType, default=[])
    doi = db.Column(db.Text, default='NA')
    acknowledgements = db.Column(db.Text, default='NA')
    number_repository_files = db.Column(db.Integer, default=0)
    size_repository_files = db.Column(db.Text, default='NA')
    source = db.Column(db.Text, default='NA')
    views = db.Column(db.Integer, default=0)
    downloads = db.Column(db.Integer, default=0)
    repository_file=db.Column(db.Text, default='')
    image_file=db.Column(db.Text, default='')

    @classmethod
    def get_unique_values(cls, colname: str) -> list | None:
        """ return list of all unique values in column """
        def flatten(xs):
            for x in xs:
                if isinstance(x, (list, tuple)):
                    yield from flatten(x)
                else:
                    yield x
        try:
            column = getattr(cls, colname)
        except AttributeError:
            return None
        return list(set(flatten(db.session.query(column).all())))
    
    @classmethod
    def purge(cls) -> None:
        """ wipe the table completely from the database and recreate it """
        cls.__table__.drop(db.engine)
        cls.__table__.create(db.engine)
    
    @classmethod
    def get_dummies(cls, n: int) -> list[Experiment]:
        """ return a list of dummy experiments for testing """
        
        def get_random_element(elements: list) -> list:
            return elements[randrange(0, len(elements))]
        
        dummy_data = []
        for i in range(1, n + 1):
            dummy_data.append({
                "title": "Dummy Experiment " + str(i),
                'description': 'This is not a real experiment',
                "creators": ['Joshua Unrau', 'Katie Lavigne', 'Martin Lepage'],
                "version": 1.0,
                "contact_person": "Josh",
                "contact_email": 'user@gmail.com',
                "modalities": [get_random_element(["fMRI", "EEG", "PET"]), "Brain"],
                'primary_software': get_random_element(["Linux", 'Windows']),
                'primary_function': get_random_element(['Cognitive', 'Sensory', 'Motor']),
                'doi': '10.1093/schbul/sbj053',
                "license": "MIT License"
            })
        return [cls(**d) for d in dummy_data]
