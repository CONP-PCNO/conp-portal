from app.models import AffiliationType, User
from flask_security import verify_password


def test_new_user(session, new_user, new_affiliation_type, app):
    """
    GIVEN a User Model
    WHEN a new User is created
    THEN check the characteristics
    """
    assert new_user.email == "example@mailinator.com"
    assert new_user.full_name=="Example User"
    assert new_user.password != "THISPassword"
    assert new_user.affiliation == "CONP"
    assert new_user.affiliation_type is not None
    assert new_user.affiliation_type == new_affiliation_type
    assert verify_password("ThisPassword", new_user.password)


def test_confirmed_at_uses_legacy_database_column(new_user):
    """
    GIVEN a Flask-Security user
    WHEN its confirmation timestamp changes
    THEN the existing database column remains synchronized
    """
    from datetime import UTC, datetime

    confirmation_time = datetime.now(UTC).replace(tzinfo=None)
    new_user.confirmed_at = confirmation_time

    assert new_user.email_confirmed_at == confirmation_time


def test_flask_security_accepts_legacy_flask_user_bcrypt_hash(app):
    """
    GIVEN a bcrypt password hash in Flask-User's existing storage format
    WHEN Flask-Security verifies it
    THEN existing accounts can keep using their current passwords
    """
    legacy_hash = (
        "$2b$12$LQv3c1yqBWVHxkd0LHAkCOP4DRIHidQKZFCb1cwPsubBvHrg/z3ji"
    )

    with app.app_context():
        assert verify_password("legacy-password", legacy_hash)

def test_user_db_model(session, new_user):
    """
    GIVEN a User Model
    WHEN a new User is created and injested into DB
    THEN check that the database user is the same
    AND the default values are set correctly
    """
    session.add(new_user)
    ## have to mock the event.listener which won't get called here
    new_user.before_commit(session)
    session.commit()
    u = User.query.filter(User.id == new_user.id).first()
    assert new_user.id > 0
    assert len(u.fs_uniquifier) == 32
    assert u.full_name == new_user.full_name
    assert u.affiliation == new_user.affiliation
    assert u.affiliation_type is not None
    assert u.affiliation_type == AffiliationType.query.filter(
                                 AffiliationType.name == "PR").first()

    assert u.has_role("member")
    session.delete(u)
    session.commit()
    u2 = User.query.filter(User.id == new_user.id).first()
    assert u2 is None
