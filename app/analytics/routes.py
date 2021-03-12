# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in the analytics blueprint
"""

import json

from flask import render_template
from flask_login import current_user
from app.analytics import analytics_bp

from app.models import MatomoDailyVisitsSummary, MatomoDailyGetPageUrlsSummary


@analytics_bp.route('/analytics')
def analytics():
    """ Analytics Route

        Route to lead to the analytics page

        Args:
            None

        Returns:
            rendered template for analytics.html for current_user
    """
    return render_template('analytics.html', title='CONP | Analytics', user=current_user)


@analytics_bp.route('/analytics/visitors')
def visitors():
    """ Analytics/Visitors Route

        Endpoint for returning analytics related to visitors to the portal

        Args:
            None

        Returns:
            Object
    """

    elements = []

    daily_visits = MatomoDailyVisitsSummary.query.order_by(
        MatomoDailyVisitsSummary.id).all()

    for v in daily_visits:
        element = {
            "id": v.id,
            "date": v.date,
            "avg_time_on_site": v.avg_time_on_site,
            "bounce_count": v.bounce_count,
            "max_actions": v.max_actions,
            "nb_actions": v.nb_actions,
            "nb_actions_per_visit": v.nb_actions_per_visit,
            "nb_uniq_visitors": v.nb_uniq_visitors,
            "nb_users": v.nb_users,
            "nb_visits": v.nb_visits,
            "nb_visits_converted": v.nb_visits_converted,
            "sum_visit_length": v.sum_visit_length
        }
        elements.append(element)

    return json.dumps(elements)


@analytics_bp.route('/analytics/views')
def views():
    """ Analytics/Views Route

        Endpoint for returning analytics related to page views on the portal

        Args:
            None

        Returns:
            Object
    """

    elements = []

    page_views = MatomoDailyGetPageUrlsSummary.query.order_by(
        MatomoDailyGetPageUrlsSummary.id).all()

    for v in page_views:
        exists = False
        for e in elements:
            label = e.get("label", None)
            if label is not None and label == v.label:
                exists = True
                e["nb_hits"] += v.nb_hits
                e["nb_visits"] += v.nb_visits
                e["nb_uniq_visitors"] += (
                    v.nb_uniq_visitors if v.nb_uniq_visitors is not None else 0)

        if not exists and v.label is not None:
            element = {
                "id": v.id,
                "url": v.url,
                "label": v.label,
                "nb_hits": v.nb_hits,
                "nb_visits": v.nb_visits,
                "nb_uniq_visitors": v.nb_uniq_visitors if v.nb_uniq_visitors is not None else 0,
            }
            elements.append(element)

    return json.dumps(elements)
