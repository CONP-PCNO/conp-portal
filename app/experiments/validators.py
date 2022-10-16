from __future__ import annotations

import re

from wtforms.form import Form
from wtforms.fields import Field
from wtforms.validators import ValidationError, URL


class ValidDOI(URL):
    def __init__(self, require_tld: bool = True, message: str ='Invalid DOI Format'):
        super().__init__(require_tld, message)
    
    def __call__(self, form: Form, field: Field) -> None:
        """ https://doi.org/10.1016/j.schres.2022.09.010
        """
        if isinstance(field.data, str) and field.data.startswith('10'):
            field.data = 'https://doi.org/' + field.data
        super().__call__(form, field)
    
def validate_doi(_, field):
    if field.data and re.match(r'^10.\d{4,9}/[-._;()/:A-Z0-9]+$', field.data) is None:
        raise ValidationError('Not a valid DOI')

