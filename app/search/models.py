import os
import json
import fnmatch
from datalad.api import Dataset as DataladDataset

class DATSDataset(object):
    def __init__(self, datasetpath):
        """
          store the datsetopath and tries to find a DATS.json file
        """

        dataset = DataladDataset(path=datasetpath)
        if not os.path.isdir(datasetpath):
            raise 'No dataset found at {}'.format(datasetpath)
        self.datasetpath = datasetpath
        self.descriptor = {}

        dirs = os.listdir(datasetpath)
        for file in dirs:
            if fnmatch.fnmatch(file.lower(), 'dats.json'):
                descriptor = os.path.join(datasetpath, file)
                break

        if descriptor == None:
            raise 'No DATS descriptor found'

        with open(descriptor, 'r') as f:
            self.descriptor = json.load(f)

    def getLogoFilepath(self):
        logopath = "app/static/img/default_dataset.jpeg"
        extraprops = self.descriptor.get('extraProperties', {})
        for prop in extraprops:
            if prop.get('category') == 'logo':
                logofilename = prop.get('values').pop().get('value', '')
                logofilepath = os.path.join(
                    self.datasetpath,
                    logofilename
                )
                if os.path.isfile(logofilepath):
                    logopath = logofilepath

        return logopath
