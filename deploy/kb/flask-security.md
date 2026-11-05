# Flask-Security deployment and maintenance

This document covers the Flask-Security 5.9.2 integration used by CONP Portal.
It is for developers preparing deployments, maintaining authentication, or
troubleshooting account-related changes.

## What changed

Flask-Security replaces Flask-User for email/password login, registration,
email confirmation, password recovery and changes, and role authorization.
The Flask-Security blueprint is named `user` to retain existing endpoint names
and URLs, including `/login`, `/register`, `/confirm`, and `/reset`. The
application's custom registration fields (full name, affiliation, affiliation
type, and agreement to the terms) remain part of registration.

The app's user model keeps the existing `users.email_confirmed_at` database
column and exposes it as Flask-Security's `confirmed_at` model attribute. The
new `fs_uniquifier` field provides the stable identity used by Flask-Security
for user sessions and tokens. Existing role membership and ORCID associations
remain in the current tables.

Active authentication templates are in `app/templates/security/`. Flask-Security
now provides its default email content; the old Flask-User email templates and
unused invite/manage-email pages were removed. The confirmation-sent page
remains application-owned.

## Configuration

Set `SECRET_KEY` and `SECURITY_PASSWORD_SALT` in the deployment's secret store.
Generate the salt with:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Keep the salt stable and distinct from `SECRET_KEY`. Production app startup
fails if the salt is empty or equals `SECRET_KEY`. Changing the salt invalidates
Flask-Security-signed confirmation, reset, and other security tokens. The
development and test configurations retain a fallback for local environments;
that fallback is not accepted in production.

`SECURITY_PASSWORD_HASH` is configured as `bcrypt`, and
`SECURITY_PASSWORD_SINGLE_HASH` is enabled. Flask-User stored bcrypt hashes
directly; Flask-Security's default additional HMAC would otherwise make those
existing hashes fail verification. Do not remove the single-hash setting or
change the configured hash scheme without planning a password migration and
testing existing account hashes.

Mail is delivered through the configured Flask-Mail settings and
`MAIL_DEFAULT_SENDER`. Verify production SMTP credentials and delivery before
relying on registration confirmation or password recovery.

## Production deployment

1. Back up the production database and verify the backup can be restored.
2. Set `SECURITY_PASSWORD_SALT` to a generated, stable secret separate from
   `SECRET_KEY`.
3. Deploy the application and install the locked dependencies from the normal
   production dependency workflow.
4. Before serving traffic from the new version, run:

   ```bash
   flask db upgrade
   ```

   Revision `5ea7104a0b6d` adds a unique, non-null `users.fs_uniquifier` value
   to every existing user and adds nullable `roles.description`. It does not
   rename or remove `email_confirmed_at`, role names, password hashes, or OAuth
   associations.
5. Restart the application workers.
6. Smoke-test an existing account's login, a newly registered account's
   confirmation email and confirmation link, password recovery and update,
   admin-only profile access, ORCID sign-in/linking, and logout. Confirm mail
   delivery and check application logs for Flask-Security configuration errors.

The new session identity is `fs_uniquifier` rather than the previous user ID.
Expect existing login sessions to require a fresh sign-in after the deployment.
Logout is now a CSRF-protected POST; update any external integrations or custom
pages that still call `/logout` with GET.

## Rollback

Prefer rolling back the application release while retaining the expanded
database schema: the previous app ignores the additional columns. The
`downgrade()` for revision `5ea7104a0b6d` drops `fs_uniquifier` and
`roles.description`; do not run it automatically after the new version has
created accounts or written role descriptions. Coordinate any schema rollback
with a verified database backup and a reviewed recovery plan.

## Tests and checks

Run authentication, model, and profile tests with:

```bash
uv run pytest -q \
  tests/blueprint_specific_tests/auth_bp_tests/test_auth_endpoints.py \
  tests/unit_tests/test_user_model.py \
  tests/blueprint_specific_tests/profile_bp_tests/test_profile_endpoints.py
```

These cover the custom registration fields, registration and confirmation
messages, email confirmation, reset email and form submission, password update,
legacy bcrypt verification, confirmation timestamp mapping, required production
salt, and profile authorization/model behavior.

Then run lint and validate the lockfile:

```bash
./lint.sh
uv lock --check
```

The broader suite also contains unrelated dataset-seeding, experiment logging,
and update-output tests. They were excluded from the migration validation run;
track them independently from the authentication migration.

To reproduce the broader validation while excluding those four tests:

```bash
uv run pytest -q --tb=short \
  --deselect=tests/database_tests/test_migrations.py::test_seed_db_test \
  --deselect=tests/database_tests/test_migrations.py::test_seed_test_datasets_db \
  --deselect=tests/unit_tests/test_experiments_quick_fixes.py::test_search_skips_an_experiment_with_missing_metadata \
  --deselect=tests/unit_tests/test_update_cli_output.py::test_update_datasets_reports_progress
```

The migration run passed 268 tests and deselected those 4 tests.

## Dependency changes

- Added `Flask-Security[fsqla,common]==5.9.2`.
- Removed `Flask-User==1.0.2.2`; its transitive `passlib` dependency is no
  longer used.
- Upgraded WTForms from the 2.3 series to 3.2, and added
  `WTForms-SQLAlchemy==0.4.2` for SQLAlchemy-backed select fields.
- Added `email-validator` as a direct requirement for Flask-Security's email
  validation.
- `uv.lock` records Flask-Security's transitive requirements, including
  `flask-principal`, `libpass`, `nh3`, `argon2-cffi`, and `bcrypt`.
