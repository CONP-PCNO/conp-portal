import os
import re
import uuid

from .. import config
from ..models import Experiment


def flatten(xs):
    for x in xs:
        if isinstance(x, (list, tuple)):
            yield from flatten(x)
        else:
            yield x


def upload_file(file) -> str:
    upload_dir = config.EXPERIMENTS_UPLOAD_DIRECTORY
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir)

    # Extract extension safely and sanitize it to alphanumeric characters only
    raw_ext = file.filename.split('.')[-1] if '.' in file.filename else ''
    file_ext = re.sub(r'[^a-zA-Z0-9]', '', raw_ext).lower()

    filename = f"{uuid.uuid4()}.{file_ext}" if file_ext else str(uuid.uuid4())
    filepath = os.path.join(upload_dir, filename)

    file.save(filepath)
    return filepath


def get_column_type(column):
    return type(Experiment.query.with_entities(column).first()[0])
