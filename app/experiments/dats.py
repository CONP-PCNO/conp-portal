from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal, Optional


def find_dats_file(dataset_path: Path) -> Path:
    dats_path_candidates: list[Path] = [
        path for path in dataset_path.iterdir() if str(path).lower() == "dats.json"
    ]
    if len(dats_path_candidates) == 0:
        raise RuntimeError(f"No DATS descriptor found under {dataset_path}")
    return dats_path_candidates[0]


class DATSExperiment:
    """Experiment backed by a DATS.json"""

    def __init__(self, dataset_path: Path, descriptor: dict[str, Any]):
        self.dataset_path = dataset_path
        self.descriptor = descriptor

    @classmethod
    def from_dataset_path(cls, dataset_path: Path):
        """Find and parse a DATS.json file to generate a DATSExperiment."""
        if not dataset_path.is_dir():
            raise RuntimeError(f"No descriptor found at {dataset_path}")

        dats_path = find_dats_file(dataset_path)
        with open(dats_path, "r", encoding="utf-8") as dats_file:
            try:
                descriptor = json.load(dats_file)
            except json.JSONDecodeError as err:
                raise RuntimeError(f"Can't parse {dats_path}") from err

        return cls(dataset_path, descriptor)

    @property
    def name(self) -> str:
        return self.dataset_path.name

    @property
    def dats_filepath(self) -> Path:
        return find_dats_file(self.dataset_path)

    def get_extra_property_values(self, category: str):
        extra_properties = self.descriptor.get("extraProperties", {})
        for property_ in extra_properties:
            if property_.get("category") == category:
                return property_.get("values")
        return None

    @property
    def logo_filepath(self) -> str:
        values = self.get_extra_property_values("logo")
        logo_filename = values.pop().get("value", "")
        logo_path = (
            logo_filename
            if logo_filename.lower().startswith("http")
            else str(self.dataset_path / logo_filename)
        )
        return logo_path

    @property
    def readme_file_path(self) -> Path:
        readme = None
        for file_ in self.dataset_path.iterdir():
            if file_.name.lower() == "readme.md":
                readme = file_
                break
        if not readme:
            raise RuntimeError("No Readme found.")

        return readme

    @property
    def creators(self) -> Optional[list[str]]:
        descriptor_creators = self.descriptor.get("creators", "")
        if isinstance(descriptor_creators, list):
            creators = [
                creator.get("fullName", creator["name"])
                for creator in descriptor_creators
                if ("name" in creator) or ("fullName" in creator)
            ]
        elif "name" in descriptor_creators:
            creators = [descriptor_creators["name"]]
        else:
            creators = [descriptor_creators]

        return creators if len(creators) > 0 else None

    @property
    def principal_investigators(self) -> Optional[list[str]]:
        def creator_is_pi(creator):
            return (
                ("roles" in creator)
                and any(
                    role["value"] == "Principal Investigator"
                    for role in creator["roles"]
                )
                and (("name" in creator) or ("fullName" in creator))
            )

        principal_investigators = []
        creators = self.descriptor.get("creators", "")
        if isinstance(creators, list):
            principal_investigators = [
                creator.get("fullName", creator["name"])
                for creator in creators
                if creator_is_pi(creator)
            ]
        elif creator_is_pi(creators):
            principal_investigators = [creators.get("fullName"), creators["name"]]
        return principal_investigators if len(principal_investigators) > 0 else None

    @property
    def primary_publications(self) -> Optional[list[dict[str, str]]]:
        def process_publication(publication):
            title = publication.get("title", "")
            if not title.endswith("."):
                title = f"{title}."
            journal = publication.get("publicationVenue", "")
            if not journal.endswith("."):
                journal = f"{journal}."
            author = (
                publication["authors"][0].get("fullName", "")
                if "authors" in publication
                else ""
            )
            if len(publication.get("authors", [])) > 1:
                author = f"{author} et al."
            doi = publication.get("identifier", {}).get("identifier", "")
            return {"title": title, "author": author, "journal": journal, "doi": doi}

        publications = self.descriptor.get("primaryPublications", {})
        if isinstance(publications, list):
            return [process_publication(publication) for publication in publications]
        if "title" in publications:
            return [process_publication(publications)]
        return None

    @property
    def authorizations(self) -> str:
        distributions = self.descriptor.get("distributions")
        if distributions is None:
            return None
        if isinstance(distributions, list):
            distribution = distributions[0]
        else:
            distribution = (
                distributions
                if distributions.get("@type", "") == "DatasetDistribution"
                else {}
            )

        authorizations = distribution.get("access", {}).get("authorizations", "")
        authorization = (
            authorizations.pop().get("value")
            if isinstance(authorizations, list)
            else None
        )
        return f"{authorization}"

    @property
    def origin(self) -> str:
        values = self.get_extra_property_values("origin")
        return (
            ", ".join([value["value"] for value in values])
            if values is not None
            else None
        )

    @property
    def contacts(self) -> str:
        values = self.get_extra_property_values("contact")
        return (
            ", ".join([value["value"] for value in values])
            if values is not None
            else None
        )

    @property
    def conp_status(self) -> Literal["CONP", "Canadian", "external"]:
        values = self.get_extra_property_values("CONP_status")
        return values[0].get("value") if values is not None else "external"

    @property
    def description(self) -> str:
        return self.descriptor.get("description")

    @property
    def file_count(self) -> int:
        values = self.get_extra_property_values("files")
        count = 0
        for value in values:
            file_count = value["value"]
            if isinstance(file_count, str):
                count += int(file_count.replace(",", ""))
            else:
                count += file_count
        return count if count > 0 else None

    @property
    def formats(self) -> list[str]:
        formats = []
        distributions = self.descriptor.get("distributions")
        if distributions is None:
            return None
        for distribution in distributions:
            formats += distribution.get("formats", [])

        return formats

    @property
    def licenses(self) -> list[str] | str:
        descriptor_licenses = self.descriptor.get("licenses")
        if isinstance(descriptor_licenses, list):
            licenses = [license.get("name") for license in descriptor_licenses]
        else:
            if "name" in descriptor_licenses:
                licenses = descriptor_licenses["name"]
            elif "$schema" in descriptor_licenses:
                licenses = descriptor_licenses["$schema"]
            elif "dataUsesConditions" in descriptor_licenses:
                licenses = descriptor_licenses["dataUsesConditions"]
            else:
                licenses = descriptor_licenses
        return licenses

    @property
    def modalities(self) -> Optional[list[str]]:
        modalities = []
        for type_ in self.descriptor.get("types", []):
            modality = type_.get("information", {}).get("value")
            if modality is not None:
                modalities.append(modality)
        return modalities if len(modalities) > 0 else None

    @property
    def keywords(self) -> Optional[list[str]]:
        keywords = []
        for keyword_dict in self.descriptor.get("keywords", []):
            keyword = keyword_dict.get("value")
            if keyword is not None:
                keywords.append(keyword)

        return keywords if len(keywords) > 0 else None

    @property
    def size(self) -> Optional[str]:
        distributions = self.descriptor.get("distributions")
        if distributions is None:
            return None
        if isinstance(distributions, list):
            distribution = distributions[0]  # Arbitrarily take the first
        else:
            distribution = (
                distributions
                if distributions.get("@type") == "DatasetDistribution"
                else {}
            )

        size = float(distribution.get("size", 0))
        unit = distribution.get("unit", {}).get("value", "")

        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
        count = 0

        while size > 1000:
            size /= 1000
            count += 1

        size = round(size, 1)
        unit = units[units.index(unit) + count]

        return f"{size} {unit}"

    @property
    def sources(self):
        distributions = self.descriptor.get("distributions")
        if distributions is None:
            return None

        if isinstance(distributions, list):
            distribution = distributions[0]
        else:
            distribution = (
                distributions
                if distributions.get("@type") == "DatasetDistribution"
                else {}
            )
        sources = distribution.get("access", {}).get("landingPage", "")
        return str(sources)

    def get_field_names(self, field: str):
        names = []
        for value in self.descriptor.get(field, []):
            name = value.get("name")
            if name is not None:
                names.append(name)
        return names if len(names > 0) else None

    @property
    def is_about(self) -> Optional[list[str]]:
        return self.get_field_names("isAbout")

    @property
    def spatial_coverage(self):
        return self.get_field_names("spatialCoverage")

    @property
    def acknowledges(self):
        acknowledges = []
        for value in self.descriptor.get("acknowledges", []):
            funders = value.get("funders")
            if funders is not None and isinstance(funders, list):
                for funder in funders:
                    if funder.get("name") is not None:
                        acknowledges.append(funder["name"])
        return acknowledges if len(acknowledges) > 0 else None

    @property
    def produced_by(self):
        produced_by = []
        field_data = self.descriptor.get("producedBy")
        if not field_data:
            return None
        if isinstance(field_data, str):
            produced_by = [field_data]
        elif isinstance(field_data, dict):
            name = field_data.get("name")
            if name is not None:
                produced_by = ["name"]
        return produced_by if len(produced_by) > 0 else None

    @property
    def subject_count(self):
        count = 0
        values = self.get_extra_property_values("origin")
        if values is None:
            return None
        for value in values:
            if isinstance(value["value"], str):
                count += int(value["value"].replace(",", ""))
            else:
                count += value["value"]
        return count if count > 0 else None

    @property
    def derived_from(self):
        values = self.get_extra_property_values("derivedFrom")
        return list(values) if ((values is not None) and (len(values) > 0)) else None

    @property
    def parent_dataset_id(self):
        parent_dataset_id = []
        values = self.get_extra_property_values("parent_dataset_id")
        if values is None:
            return None
        for value in values:
            if value.get("value") is not None:
                parent_dataset_id.append(value["value"])
        return parent_dataset_id if len(parent_dataset_id) > 0 else None

    @property
    def version(self):
        return self.descriptor.get("version")

    @property
    def dates(self):
        dates = {}
        for value in self.descriptor.get("dates", {}):
            date = value.get("date", "")
            date_type = value.get("type", {}).get("value", "").title()
            dates[date_type] = date
        return dates if len(dates) > 0 else None

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
