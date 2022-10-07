from __future__ import annotations

from ..models import Experiment

class SearchEngine:

    def __init__(self) -> None:
        pass

    def search(self, search_term: str, experiments: list[Experiment]):
        matching_ids = []
        for experiment in experiments:
            if self.assess_title(search_term, experiment):
                matching_ids.append(experiment.id)
        return matching_ids

    def assess_title(self, search_term: str, experiment: Experiment) -> bool:
        return search_term.lower() in experiment.title.lower()

