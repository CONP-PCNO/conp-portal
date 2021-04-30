# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes in the analytics blueprint
"""

import json

from flask import render_template, request
from flask_login import current_user
from app.analytics import analytics_bp
from app.pipelines import pipelines

from app.models import MatomoDailyVisitsSummary, MatomoDailyGetDatasetPageViewsSummary, MatomoDailyGetSiteSearchKeywords, MatomoDailyGetPageUrlsSummary


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


@analytics_bp.route('/analytics/datasets/views')
def datasets_views():
    """ Analytics/Datasets/Views Route

        Endpoint for returning analytics related to dataset page views on the portal

        Args:
            None

        Returns:
            Object
    """

    elements = []

    page_views = []

    id = request.args.get('id', None)

    if id is not None:
        page_views = MatomoDailyGetDatasetPageViewsSummary.query.filter_by(
            dataset_id=id).all()

    else:
        page_views = MatomoDailyGetDatasetPageViewsSummary.query.order_by(
            MatomoDailyGetDatasetPageViewsSummary.id).all()

    for v in page_views:
        exists = False
        for e in elements:
            dataset_id = e.get("dataset_id", None)
            if dataset_id is not None and dataset_id == v.dataset_id:
                exists = True
                e["nb_hits"] += v.nb_hits
                e["nb_visits"] += v.nb_visits
                e["nb_uniq_visitors"] += (
                    v.nb_uniq_visitors if v.nb_uniq_visitors is not None else 0)

        if not exists and v.dataset_id is not None:
            element = {
                "dataset_id": v.dataset_id,
                "url": v.url,
                "label": v.label,
                "nb_hits": v.nb_hits,
                "nb_visits": v.nb_visits,
                "nb_uniq_visitors": v.nb_uniq_visitors if v.nb_uniq_visitors is not None else 0,
            }
            elements.append(element)

    elements.sort(key=lambda e: e["nb_hits"], reverse=True)

    return json.dumps(elements)


@analytics_bp.route('/analytics/pipelines/views')
def pipelines_views():
    """ Analytics/Pipelines/Views Route

        Endpoint for returning analytics related to pipeline page views on the portal

        Args:
            None

        Returns:
            Object
    """

    elements = []

    page_views = []

    id = request.args.get('id', None)

    if id is not None:
        page_views = MatomoDailyGetPageUrlsSummary.query.filter_by(
            label="/pipeline?id=" + id).all()

    else:
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

        if not exists and v.label is not None and "/pipeline?id=" in v.label:
            if pipelines.get_title_from_id(v.label.split('id=')[1]):
                element = {
                    "url": v.url,
                    "label": v.label,
                    "title": pipelines.get_title_from_id(v.label.split('id=')[1]),
                    "nb_hits": v.nb_hits,
                    "nb_visits": v.nb_visits,
                    "nb_uniq_visitors": v.nb_uniq_visitors if v.nb_uniq_visitors is not None else 0,
                }
                elements.append(element)

    elements.sort(key=lambda e: e["nb_hits"], reverse=True)

    return json.dumps(elements)


@analytics_bp.route('/analytics/keywords')
def keywords():
    """ Analytics/Keywords Route

        Endpoint for returning analytics related to datset page views on the portal

        Args:
            None

        Returns:
            Object
    """

    elements = []

    keywords = MatomoDailyGetSiteSearchKeywords.query.order_by(
        MatomoDailyGetSiteSearchKeywords.id).all()

    for v in keywords:
        exists = False
        for e in elements:
            label = e.get("label", None)
            if label is not None and label == v.label:
                exists = True
                e["nb_hits"] += v.nb_hits

        if not exists and v.label is not None:
            element = {
                "label": v.label,
                "nb_hits": v.nb_hits,
            }
            elements.append(element)

    # Filter out short keywords
    elements = list(filter(lambda e: len(e['label']) > 2, elements))

    elements.sort(key=lambda e: e["nb_hits"], reverse=True)

    return json.dumps(elements)
