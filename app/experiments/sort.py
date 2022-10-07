from collections import UserDict

from ..models import Experiment

class SortKey:

    options = {
        "title_asc": {
            "column": Experiment.title,
            "label": "Title (A-Z)"
        }, 
        "title_desc": {
            "column": Experiment.title.desc(),
            "label": "Title (Z-A)"
        }
    }

    def __init__(self, value: str) -> None:
        if value not in self.options.keys():
            raise ValueError(f'Invalid value for sort key: {value}')
        self.value = value
    
    def __str__(self) -> str:
        return self.options[self.value]['label']
    
    def column(self):
        return self.options[self.value]['column']