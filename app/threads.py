"""Threading Module

Module that contains the threaded pipeline searching functions
"""
import json
import logging
import os
import threading

from boutiques.puller import Puller
from boutiques.searcher import Searcher

# Create a dedicated logger for this specific module
logger = logging.getLogger(__name__)


class UpdatePipelineData(threading.Thread):
    """
        Class that handles the threaded updating of the Pipeline
        registrty from Zenodo
    """
    def __init__(self):
        super().__init__()
        if not os.path.exists('logs'):
            os.makedirs('logs')
        logger.basicConfig(filename='logs/update_pipeline_thread.log', level=logger.INFO)

    def run(self):
        try:
            boutique_cache_dir = os.path.join(
                os.path.expanduser('~'),
                ".cache",
                "boutiques",
                "production"
            )
            # first search for all descriptors
            searcher = Searcher(query=None, max_results=9999, no_trunc=True, verbose=True)
            all_descriptors = searcher.search()
            # then pull every single descriptor
            all_descriptor_ids = [x["ID"] for x in all_descriptors]
            files = Puller(all_descriptor_ids).pull()

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
