import re

from wtforms.validators import ValidationError

def flatten(xs):
  for x in xs:
    if isinstance(x, (list, tuple)):
      yield from flatten(x)
    else:
      yield x

def validate_doi(_, field):
    if field.data and re.match(r'^10.\d{4,9}/[-._;()/:A-Z0-9]+$', field.data) is None:
        raise ValidationError('Not a valid DOI')
