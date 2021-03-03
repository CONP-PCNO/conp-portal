# -*- coding: utf-8 -*-
from app.utils import utils_bp
from app.models import AffiliationType
from wtforms import SelectMultipleField


def possible_affiliation_types():
    return AffiliationType.query


class RoleMultiField(SelectMultipleField):
    def pre_validation(self, form):
        pass


@utils_bp.app_template_filter('set_selected_for_multiselect')
def set_selected_for_multiselect(text, values):
    for v in values:
        tmpTxt = text.replace('value="{}"'.format(v.id),
                              'selected value="{}"'.format(v.id))
    text = tmpTxt
    return text
