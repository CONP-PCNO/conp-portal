from boutiques.searcher import Searcher
from boutiques.puller import Puller
import threading
import json
import os


class UpdatePipelineData(threading.Thread):

    def __init__(self, path):
        super(UpdatePipelineData, self).__init__()
        self.cache_dir = path

    def run(self):

        #first search for all descriptors
        searcher = Searcher(query="", max_results=100, no_trunc=True)
        all_descriptors = searcher.search()

        #if cache doesn't exist, make it
        if not os.path.exists(self.cache_dir):
            os.makedirs(".cache/boutiques")

        #store data in cache
        with open(os.path.join(self.cache_dir, "all_descriptors.json"), "w") as f:
            json.dump(all_descriptors, f, indent=4)

        #then pull every single descriptor and store in cache
        for descriptor in all_descriptors:
            Puller(zid=descriptor["ID"]).pull()
