"""Threading Module

Module that contains the threaded pipeline searching functions
"""
import json
import logging
import os
import threading

import requests
from boutiques.searcher import Searcher
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create a dedicated logger for this specific module
logger = logging.getLogger(__name__)

# Zenodo search used by Boutiques (`bosh search`) to list published descriptors.
ZENODO_RECORDS_API = "https://zenodo.org/api/records/"
BOUTIQUES_QUERY = (
    "keywords:(/Boutiques/) AND keywords:(/schema.*/) AND keywords:(/version.*/)"
)
# Zenodo rejects unauthenticated searches asking for more than 25 results per
# page (HTTP 400). Boutiques 0.5.28 asks for 9999 in one page, in both
# `bosh search` and `bosh pull`, so both fail; 0.5.33 caps the result at 25.
# We therefore page through Zenodo ourselves and download each descriptor
# from the link the search returns.
ZENODO_PAGE_SIZE = 25
# Without an explicit sort, Zenodo's relevance ordering is not stable across
# pages, so records repeat and others are skipped. Creation order is stable.
ZENODO_SORT = "oldest"


def _zenodo_session():
    """HTTP session that retries transient Zenodo failures."""
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504))
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def search_all_descriptors(timeout=60):
    """Return (entries, file_links) for every published Boutiques descriptor.

    ``entries`` have the same shape as ``Searcher(verbose=True).search()``;
    ``file_links`` maps each entry ID ("zenodo.<id>") to its descriptor file URL.
    """
    searcher = Searcher(query=None, max_results=9999, no_trunc=True, verbose=True)
    session = _zenodo_session()
    entries, file_links = [], {}
    page = 1
    while True:
        response = session.get(
            ZENODO_RECORDS_API,
            params={
                "q": BOUTIQUES_QUERY,
                "file_type": "json",
                "type": "software",
                "page": page,
                "size": ZENODO_PAGE_SIZE,
                "sort": ZENODO_SORT,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        hits = payload["hits"]["hits"]
        if not hits:
            break
        for hit in hits:
            # Some records lack fields that Boutiques' formatter assumes.
            metadata = hit.setdefault("metadata", {})
            metadata.setdefault("description", "")
            metadata.setdefault("keywords", [])
            hit.setdefault("stats", {})
            try:
                entry = searcher.create_results_list_verbose({"hits": {"hits": [hit]}})[0]
                if entry["ID"] in file_links:
                    continue  # already seen on an earlier page
                file_links[entry["ID"]] = hit["files"][0]["links"]["self"]
            except (KeyError, IndexError, TypeError):
                logger.exception("Skipping malformed Zenodo record %s", hit.get("id"))
                continue
            entries.append(entry)
        if page * ZENODO_PAGE_SIZE >= payload["hits"]["total"]:
            break
        page += 1
    entries.sort(key=lambda d: d["DOWNLOADS"], reverse=True)
    return entries, file_links


def pull_descriptors(entries, file_links, cache_dir, timeout=60):
    """Download each descriptor into the Boutiques cache (zenodo-<id>.json),
    reusing files already cached, as `bosh pull` does. Returns the paths in
    the same order as ``entries``, and the entries that could be pulled."""
    os.makedirs(cache_dir, exist_ok=True)
    session = _zenodo_session()
    paths, kept = [], []
    for entry in entries:
        zid = entry["ID"].split(".", 1)[1]
        path = os.path.join(cache_dir, f"zenodo-{zid}.json")
        if not os.path.isfile(path):
            try:
                response = session.get(file_links[entry["ID"]], timeout=timeout)
                response.raise_for_status()
                json.loads(response.content)  # refuse anything that is not JSON
                with open(path, "wb") as f:
                    f.write(response.content)
            except (requests.RequestException, ValueError, KeyError):
                logger.exception("Could not pull descriptor %s", entry["ID"])
                continue
        paths.append(path)
        kept.append(entry)
    return paths, kept


class UpdatePipelineData(threading.Thread):
    """
        Class that handles the threaded updating of the Pipeline
        registrty from Zenodo
    """
    def __init__(self):
        super().__init__()
        if not os.path.exists('logs'):
            os.makedirs('logs')
        logging.basicConfig(filename='logs/update_pipeline_thread.log', level=logging.INFO)

    def run(self):
        try:
            boutique_cache_dir = os.path.join(
                os.path.expanduser('~'),
                ".cache",
                "boutiques",
                "production"
            )
            # first search for all descriptors
            all_descriptors, file_links = search_all_descriptors()
            logger.info("Found %d Boutiques descriptors on Zenodo", len(all_descriptors))
            # then pull every single descriptor
            files, all_descriptors = pull_descriptors(
                all_descriptors, file_links, boutique_cache_dir)

            # fetch every single descriptor into one file
            detailed_all_descriptors = []
            for f in files:
                with open(f) as file:
                    detailed_all_descriptors.append(json.load(file))

            # store data in cache
            with open(os.path.join(boutique_cache_dir, "all_descriptors.json"), "w") as f:
                json.dump(all_descriptors, f, indent=4)

            with open(os.path.join(boutique_cache_dir, "detailed_all_descriptors.json"), "w") as f:
                json.dump(detailed_all_descriptors, f, indent=4)

        except Exception:
            logger.exception("An exception occurred in the thread.")
