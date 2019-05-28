from threading import Thread
from boutiques import search
import json


class UpdatePipelineData(Thread):

    def run(self):
        with open(".cache/boutiques/pipelineData.json", "w") as f:
            data = search("-m 1000", "-nt")
            json.dump(data, f, indent=4)
