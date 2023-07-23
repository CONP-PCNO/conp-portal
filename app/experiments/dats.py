from typing import List, Optional

from app.dats import DATSObject


class DATSExperiment(DATSObject):
    def find_extra_property(self, category) -> list:
        for prop in self.descriptor.get("extraProperties", []):
            if prop.get("category", "") == category:
                return [value_dict["value"] for value_dict in prop.get("values", [])]
        return []

    @property
    def function_assessed(self) -> Optional[str]:
        try:
            return self.find_extra_property("experimentFunctionAssessed").pop()
        except KeyError:
            return None

    @property
    def languages(self) -> Optional[List[str]]:
        return self.find_extra_property("experimentLanguages")

    @property
    def validation(self) -> Optional[List[str]]:
        """Assuming one type of validation for now."""
        return self.find_extra_property("experimentValidation")

    @property
    def accessibility(self) -> Optional[List[str]]:
        return self.find_extra_property("experimentAccessibility")

    @property
    def experiment_modalities(self):
        return self.find_extra_property("experimentModalities")

    @property
    def device_requirements(self) -> Optional[List[str]]:
        return self.find_extra_property("experimentRequiredDevices")

    @property
    def software_requirements(self) -> Optional[List[str]]:
        return self.find_extra_property("experimentRequiredSoftware")

    @property
    def other_requirements(self) -> Optional[List[str]]:
        return self.find_extra_property("experimentRequiredOther")
