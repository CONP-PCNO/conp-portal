
from app.dats import DATSObject


class DATSExperiment(DATSObject):
    def find_extra_property(self, category) -> list:
        for prop in self.descriptor.get("extraProperties", []):
            if prop.get("category", "") == category:
                return [value_dict["value"] for value_dict in prop.get("values", [])]
        return []

    @property
    def function_assessed(self) -> str | None:
        try:
            return self.find_extra_property("experimentFunctionAssessed").pop()
        except (KeyError, IndexError):   # no value: pop() on an empty list
            return None

    @property
    def languages(self) -> list[str] | None:
        return self.find_extra_property("experimentLanguages")

    @property
    def validation(self) -> list[str] | None:
        """Assuming one type of validation for now."""
        return self.find_extra_property("experimentValidation")

    @property
    def accessibility(self) -> list[str] | None:
        return self.find_extra_property("experimentAccessibility")

    @property
    def experiment_modalities(self):
        return self.find_extra_property("experimentModalities")

    @property
    def device_requirements(self) -> list[str] | None:
        return self.find_extra_property("experimentRequiredDevices")

    @property
    def software_requirements(self) -> list[str] | None:
        return self.find_extra_property("experimentRequiredSoftware")

    @property
    def other_requirements(self) -> list[str] | None:
        return self.find_extra_property("experimentRequiredOther")

    # Field names as the DATS editor writes them (2023 experiment mode).
    @property
    def validation_measures(self) -> list:
        return [v for v in _flat(self.find_extra_property("experimentValidationMeasures")) if v]

    @property
    def validation_populations(self) -> list:
        return [v for v in _flat(self.find_extra_property("experimentValidationPopulations")) if v]

    @property
    def stimuli(self) -> list:
        return [v for v in _flat(self.find_extra_property("experimentStimuli")) if v]

    @property
    def additional_requirements(self) -> list:
        """experimentAdditionalRequirements (the editor nests it in lists)."""
        return [v for v in _flat(self.find_extra_property("experimentAdditionalRequirements")
                                 + self.find_extra_property("experimentRequiredOther")) if v]


def _flat(values):
    """Values as a flat list of non-empty strings (some records nest lists)."""
    out = []
    for v in values or []:
        if isinstance(v, (list, tuple)):
            out.extend(_flat(v))
        elif isinstance(v, dict):
            out.extend(_flat([v.get('value')]))
        elif v is not None and str(v).strip():
            out.append(str(v).strip())
    return out
