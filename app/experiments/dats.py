from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal, Optional


def find_dats_file(dataset_root: Path) -> Path:
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

    @property
    def logo_filepath(self) -> str:
        extra_props = self.descriptor.get("extraProperties", {})
        for prop in extra_props:
            if prop.get("category") != "logo":
                continue
            logo_filename = prop["values"].pop().get("value", "")
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
        creators = self.descriptor.get("creators", "")
        if isinstance(creators, list):
            principal_investigators = [
                creator.get("fullName", creator["name"])
                for creator in creators
                if ("roles" in creator)
                and any(
                    role["value"] == "Principal Investigator"
                    for role in creator["roles"]
                )
                and (("name" in creator) or ("fullName" in creator))
            ]
        elif (
            ("roles" in creators)
            and any(
                role["value"] == "Principal Investigator" for role in creators["roles"]
            )
            and (("name" in creators) or ("fullName" in creators))
        ):
            principal_investigators = [creators.get("fullName"), creators["name"]]
        return principal_investigators if len(principal_investigators) > 0 else None


    logo_filepath: str = logo_filepath
    readme_filepath: Path = readme_filepath
    creators: Optional[list[str]] = self.creators
    principal_investigators: Optional[list[str]] = self.principal_investigators
    primary_publications: Optional[
        list[dict[str, str]]
    ] = primary_publications
    authorizations: str = authorizations
    origin: Optional[str] = origin
    contacts: str = contacts
    conp_status: Literal["CONP", "Canadian", "external"] = conp_status
    description: str = description
    file_count: int = file_count
    formats: list[str] = formats
    licenses: list[str] = licenses
    modalities: list[str] = modalities
    keywords: list[str] = keywords
    size: str = size
    sources: str = sources
    dimensions: list[str] = dimensions
    is_about: list[str] = is_about
    acknowedges: list[str] = acknowledges
    spatial_converage: list[str] = spatial_coverage
    produced_by: list[str] = produced_by
    subject_count: list[str] = subject_count
    derived_from: list[str] = derived_from
