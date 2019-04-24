from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone
eastern = timezone('US/Eastern')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, index=True, unique=True)
    oauth_id = db.Column(db.String(256), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    is_whitelisted = db.Column(db.Boolean, default=False, nullable=False)
    is_pi = db.Column(db.Boolean, default=False, nullable=False)
    is_account_expired = db.Column(db.Boolean, default=False, nullable=False)
    affiliation = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.String(64), index=True, unique=True)
    annex_uuid = db.Column(db.String(64), index=True, unique=True)
    datalad_remote_annex_uuid = db.Column(db.String(64), index=True, unique=True)
    owner_id = db.Column(db.Integer, index=True)
    download_path = db.Column(db.String(64), index=True)
    image = db.Column(db.LargeBinary, default=None)
    name = db.Column(db.String(256), index=True)
    modality = db.Column(db.String(64), index=True)
    version = db.Column(db.String(128), index=True)
    format = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64), index=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))
    is_private = db.Column(db.Boolean, index=True)

    def __repr__(self):
        return '<Dataset {}>'.format(self.name)

class DatasetStats(db.Model):
    __tablename__ = 'dataset_stats'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, index=True, unique=True)
    size = db.Column(db.Integer, index=True)
    files = db.Column(db.Integer, index=True)
    sources = db.Column(db.Integer, index=True)
    num_subjects = db.Column(db.Integer, index=True)
    num_downloads = db.Column(db.Integer, index=True)
    num_likes = db.Column(db.Integer, index=True)
    num_views = db.Column(db.Integer, index=True)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))

class Pipeline(db.Model):
    __tablename__ = 'pipelines'

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, index=True, unique=True)
    owner_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(256), index=True)
    version = db.Column(db.String(128), index=True)
    is_private = db.Column(db.Boolean, index=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=eastern))

    def __repr__(self):
        return '<Pipeline {}>'.format(self.name)
