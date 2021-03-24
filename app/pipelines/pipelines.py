# -*- coding: utf-8 -*-
import json
import os


def get_pipelines_from_cache(search_query=None):
    cache_dir = os.path.join(os.path.expanduser(
        '~'), ".cache", "boutiques", "production")
    all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
    all_detailed_desc_path = os.path.join(
        cache_dir, "detailed_all_descriptors.json")

    # fetch data from cache
    with open(all_desc_path, "r") as f:
        all_descriptors = json.load(f)

    with open(all_detailed_desc_path, "r") as f:
        detailed_all_descriptors = json.load(f)

    if search_query not in ("", '', None):
        pipelines = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
            if search_query in (
                (str(descriptor.values())
                    + str(detailed_all_descriptors[d_index]["tags"].values())).lower()
                if "tags" in detailed_all_descriptors[d_index] else
                str(descriptor.values()).lower()
            )
        ]
    else:
        pipelines = [
            {**descriptor, **detailed_all_descriptors[d_index]}
            for d_index, descriptor in enumerate(all_descriptors)
        ]

    return pipelines


def get_title_from_id(pipeline_id):
    pipelines = get_pipelines_from_cache()

    filtered_pipelines = list(
        filter(lambda e: e['ID'] == pipeline_id, pipelines))

    title = None
    if len(filtered_pipelines) > 0:
        pipeline = filtered_pipelines[0]
        title = pipeline.get("TITLE", None)

    return title
