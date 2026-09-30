from wtforms import SelectMultipleField

from app.models import AffiliationType
from app.utils import utils_bp


def possible_affiliation_types():
    return AffiliationType.query


class RoleMultiField(SelectMultipleField):
    def pre_validation(self, form):
        pass


@utils_bp.app_template_filter('set_selected_for_multiselect')
def set_selected_for_multiselect(text, values):
    for v in values:
        tmpTxt = text.replace(f'value="{v.id}"',
                              f'selected value="{v.id}"')
    text = tmpTxt
    return text
