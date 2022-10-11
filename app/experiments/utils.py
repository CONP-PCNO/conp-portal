from __future__ import annotations

import os
import re
import uuid

from werkzeug.utils import secure_filename
from wtforms import FileField
from wtforms.validators import ValidationError

from .. import config

def flatten(xs):
  for x in xs:
    if isinstance(x, (list, tuple)):
      yield from flatten(x)
    else:
      yield x

def validate_doi(_, field):
    if field.data and re.match(r'^10.\d{4,9}/[-._;()/:A-Z0-9]+$', field.data) is None:
        raise ValidationError('Not a valid DOI')


def upload_file(field: FileField) -> str | None:
  if field.data.filename:
    upload_dir = getattr(config, 'EXPERIMENTS_UPLOAD_DIRECTORY')
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir)
    file_ext = field.data.filename.split('.')[-1]
    filename = secure_filename(f"{uuid.uuid4()}.{file_ext}")
    field.data.save(os.path.join(upload_dir, filename))
    return filename
  return None

