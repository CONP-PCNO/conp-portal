# -*- coding: utf-8 -*-
"""Threading Module

Module that contains the threaded pipeline searching functions
"""
from boutiques.searcher import Searcher
from boutiques.puller import Puller
import threading
import json
import os
import logging


class UpdatePipelineData(threading.Thread):
    """
        Class that handles the threaded updating of the Pipeline
        registrty from Zenodo
    """
    def __init__(self):
        super(UpdatePipelineData, self).__init__()
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
            searcher = Searcher(query=None, max_results=9999, no_trunc=True, verbose=True)
            all_descriptors = searcher.search()
            # then pull every single descriptor
            all_descriptor_ids = list(map(lambda x: x["ID"], all_descriptors))
            files = Puller(all_descriptor_ids).pull()

            # fetch every single descriptor into one file
            detailed_all_descriptors = list(map(lambda f: json.load(open(f, 'r')), files))

            # store data in cache
            with open(os.path.join(boutique_cache_dir, "all_descriptors.json"), "w") as f:
                json.dump(all_descriptors, f, indent=4)

            with open(os.path.join(boutique_cache_dir, "detailed_all_descriptors.json"), "w") as f:
                json.dump(detailed_all_descriptors, f, indent=4)

        except Exception as e:
            logging.exception("An exception occurred in the thread:{0}.".format(e))
