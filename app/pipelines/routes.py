import json, os, time
from app.threads import UpdatePipelineData

from flask import render_template, request
from flask_login import current_user

from app.pipelines import pipelines_bp

@pipelines_bp.route('/pipelines')
def pipelines():
    return render_template('pipelines.html', title='CONP | Tools & Pipelines')

@pipelines_bp.route('/pipeline-search', methods=['GET'])
def pipeline_search():
    if request.method == 'GET':

        authorized = True if current_user.is_authenticated else False

        # initialize variables
        search_query = request.args.get("search").lower()
        sort_key = request.args.get("sortKey") or "downloads-desc"
        cache_dir = os.path.join(os.path.expanduser('~'), ".cache", "boutiques")
        all_desc_path = os.path.join(cache_dir, "all_descriptors.json")
        all_detailed_desc_path = os.path.join(cache_dir, "detailed_all_descriptors.json")

        # fetch data from cache
        with open(all_desc_path, "r") as f:
            all_descriptors = json.load(f)

        with open(all_detailed_desc_path, "r") as f:
            detailed_all_descriptors = json.load(f)

        # if the cache data older than 5min or 300 seconds, update in background
        delta = time.time() - os.path.getmtime(all_desc_path)
        if delta > 300:
            print("Pipeline database older than 5 minutes, updating...")
            UpdatePipelineData(path=cache_dir).start()

        # search cache with search query else return everything
        if search_query not in ("", '', None):
            elements = [
                {**descriptor, **detailed_all_descriptors[d_index]}
                for d_index, descriptor in enumerate(all_descriptors)
                if search_query in (
                    (str(descriptor.values()) + str(detailed_all_descriptors[d_index]["tags"].values())).lower()
                    if "tags" in detailed_all_descriptors[d_index] else
                    str(descriptor.values()).lower()
                )
            ]
        else:
            elements = [
                {**descriptor, **detailed_all_descriptors[d_index]}
                for d_index, descriptor in enumerate(all_descriptors)
            ]

        # sort, make all keys lowercase and without hyphen
        elements = [{k.lower().replace("-", ""): v for k, v in element.items()} for element in elements]
        elements.sort(
            key=lambda x: x["downloads"],
            reverse=True if sort_key == "downloads-desc" or sort_key == "title" else False
        )

        # if element has online platform url, retrieve the cbrain one, else take the first one and set logo
        for element in elements:
            if "onlineplatformurls" in element:
                for url in element["onlineplatformurls"]:
                    if "cbrain" in url:
                        element["onlineplatformurls"] = url
                        element["img"] = "static/img/run_on_cbrain_green.png"
                        break
                else:
                    element["onlineplatformurls"] = element["onlineplatformurls"][0]
                    element["img"] = "static/img/globe-solid-green.png"
            else:
                element["img"] = "static/img/globe-solid-grey.png"

        # construct payload
        payload = {
            "authorized": authorized,
            "total": len(elements),
            "sortKeys": [
                {
                    "key": "downloads-desc",
                    "label": "Downloads: High to Low"
                },
                {
                    "key": "downloads-asc",
                    "label": "Downloads: Low to High"
                }
            ],
            "elements": elements
        }

        return json.dumps(payload)

@pipelines_bp.route('/share')
def share():
    return render_template('share.html', title='CONP | Share a Dataset', user=current_user)

@pipelines_bp.route('/tools')
def tools():
    return render_template('tools.html', title='CONP | Tools & Pipelines', user=current_user)
