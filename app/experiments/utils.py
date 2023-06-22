import os
import uuid

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .. import config
from ..models import Experiment

def flatten(xs):
  for x in xs:
    if isinstance(x, (list, tuple)):
      yield from flatten(x)
    else:
      yield x

def upload_file(file: FileStorage) -> str:
  upload_dir = getattr(config, 'EXPERIMENTS_UPLOAD_DIRECTORY')
  if not os.path.isdir(upload_dir):
      os.makedirs(upload_dir)
  file_ext = file.filename.split('.')[-1]
  filepath = os.path.join(upload_dir, secure_filename(f"{uuid.uuid4()}.{file_ext}"))
  file.save(filepath)
  return filepath

def get_column_type(column):
  return type(Experiment.query.with_entities(column).first()[0])

