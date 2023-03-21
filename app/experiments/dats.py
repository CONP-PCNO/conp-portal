from __future__ import annotations

from typing import Optional

from app.dats import DATSObject


class DATSExperiment(DATSObject):
    @property
    def experiment_properties(self) -> dict:
        return self.descriptor.get("extraProperties", {}).get(
            "experimentProperties", {}
        )

    @property
    def function_assessed(self) -> Optional[str]:
        return self.experiment_properties.get("functionAssessed")

    @property
    def languages(self) -> Optional[list[str]]:
        return self.experiment_properties.get("languages")

    @property
    def validation(self) -> Optional[list[str]]:
        """Assuming one type of validation for now."""
        return self.experiment_properties.get("validation")

    @property
    def accessibility(self) -> Optional[list[str]]:
        return self.experiment_properties.get("accessibility")

    @property
    def requirements(self) -> dict:
        return self.experiment_properties.get("requirements", {})

    @property
    def platform_requirements(self) -> Optional[list[str]]:
        return self.requirements.get("platforms")

    @property
    def device_requirements(self) -> Optional[list[str]]:
        return self.requirements.get("devices")

    @property
    def software_requirements(self) -> Optional[list[dict]]:
        return self.requirements.get("software")

    @property
    def other_requirements(self) -> Optional[list[str]]:
        return self.requirements.get("other")
