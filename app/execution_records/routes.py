# -*- coding: utf-8 -*-
""" Routes Module

    Currently this module contains all of the routes for the execution_records blueprint
"""
import json
import os
from flask import render_template, request
from flask_login import current_user
from app.execution_records import execution_records_bp
import zipfile


@execution_records_bp.route('/execution-records')
def execution_records():

    """ Execution Records Route

        The route that leads to the execution record page

        Args:
            page: the page that you want to display (default: 1)
            max_per_page: the number of items per page (default: 10)

        Returns:
            Rendered template for execution-records.html
    """
    page = 1
    max_per_page = request.args.get('max_per_page') or 10
    if max_per_page != 'All':
        max_per_page = int(max_per_page)
    searchPipelineName = ""
    searchDatasetName = ""

    filters = {
        "page": page,
        "max_per_page": max_per_page,
        "searchPipelineName": searchPipelineName,
        "searchDatasetName": searchDatasetName,
    }

    return render_template('execution-records.html',
                           title='CONP Portal | Pipeline Execution Records',
                           filters=filters)


@execution_records_bp.route('/execution-records-search', methods=['GET'])
def execution_records_search():
    authorized = True if current_user.is_authenticated else False

    elements = []

    with open("app/static/execution-records/execution-records.json") as f:
        data = json.load(f)
    for item in data:
        newElement = {
            "pipelineName": item["pipeline"],
            "pipelineUrl": item["pipeline_link"],
            "datasetName": item["dataset"],
            "datasetUrl": item["dataset_link"],
            "executionRecord": item["status"],
            "executionRecordUrl": item["status_link"]
        }
        elements += [newElement]

    # get request variables
    pipelineSearchQuery = request.args.get(
        "searchPipelineName").lower() if request.args.get("searchPipelineName") else ''
    datasetSearchQuery = request.args.get(
        "searchDatasetName").lower() if request.args.get("searchDatasetName") else ''

    max_per_page = len(elements)
    if request.args.get('max_per_page') != 'All':
        max_per_page = int(request.args.get("max_per_page") or 999999)

    elements_on_page = []
    for item in elements:
        if len(elements_on_page) >= max_per_page:
            continue
        if pipelineSearchQuery:
            if datasetSearchQuery:
                if (pipelineSearchQuery in item["pipelineName"].lower()) and (datasetSearchQuery in item["datasetName"].lower()):
                    elements_on_page += [item].copy()
            else:
                if (pipelineSearchQuery in item["pipelineName"].lower()):
                    elements_on_page += [item].copy()
        else:
            if datasetSearchQuery:
                if (datasetSearchQuery in item["datasetName"].lower()):
                    elements_on_page += [item].copy()
            else:
                elements_on_page = elements.copy()
                continue

    # extract the appropriate page
    page = int(request.args.get("page") or 1)

    if max_per_page is not None:
        if len(elements_on_page) > max_per_page:
            start_index = (page - 1) * max_per_page
            end_index = start_index + max_per_page
            if end_index > len(elements_on_page):
                end_index = len(elements_on_page)
            elements_on_page = elements_on_page[start_index:end_index]

    # construct payload
    payload = {
        "authorized": authorized,
        "total": len(elements),
        "elements": elements_on_page
    }

    return json.dumps(payload)


@execution_records_bp.route('/execution-record-info', methods=['GET'])
def execution_record_info():

    """ Execution Records Route

        The route that leads to the execution record page

        Args:
            executionRecordUrl: the page that you want to display (default: 1)
            max_per_page: the number of items per page (default: 10)

        Returns:
            Rendered template for execution-records.html
    """

    file_name = request.args.get('file-name')
    archived_file_name = os.path.join("app/static/execution-records-details/", file_name + ".json.zip")

    archiveFile = zipfile.ZipFile(archived_file_name, 'r')
    fileContent = archiveFile.read(file_name + ".json")
    fileContent = json.loads(fileContent.decode("utf-8"))
    fileContent = json.dumps(fileContent, indent=4, sort_keys=True)

    return render_template('execution-record-info.html',
                           title='CONP Portal | Pipeline Execution Record Informations',
                           jsonfile=fileContent.replace('\n', '<br>').replace('    ', '&emsp;'))
