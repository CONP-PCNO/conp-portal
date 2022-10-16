from __future__ import annotations

import os
import uuid

from werkzeug.utils import secure_filename
from wtforms import FileField

from .. import config
from ..models import Experiment

def flatten(xs):
  for x in xs:
    if isinstance(x, (list, tuple)):
      yield from flatten(x)
    else:
      yield x

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

def get_column_type(column):
  return type(Experiment.query.with_entities(column).first()[0])

