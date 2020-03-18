# -*- coding: utf-8 -*-
import pytest
from app.search.models import DATSDataset


def test_datsdataset_jsonld(new_dataset):
    """
    Check json-ld snippet for Google dataset search is correct
    """
    assert new_dataset.dataset_id == "8de99b0e-5f94-11e9-9e05-52545e9add8e"
    assert new_dataset.fspath == './test/test_dataset'
    dats_dataset = DATSDataset(datasetpath=new_dataset.fspath)
    assert type(dats_dataset.schema_org_metadata) is dict
    assert dats_dataset.version == "1.0"
    assert dats_dataset.schema_org_metadata["@context"] == "https://schema.org/"
    assert dats_dataset.schema_org_metadata["@type"] == "Dataset"
    assert dats_dataset.schema_org_metadata["name"] == "Multicenter Single Subject Human MRI Phantom"
    assert dats_dataset.schema_org_metadata["description"] == "Human Brain phantom scans, Multiple MRI"\
                                                       " scans of a single human phantom over 11"\
                                                       " years, T1 weighted images and others on"\
                                                       " 13 scanner in 6 sites accross North America."\
                                                       " The data are available in minc format."
    assert dats_dataset.schema_org_metadata["version"] == "1.0"
    assert type(dats_dataset.schema_org_metadata["license"]) is list
    assert dats_dataset.schema_org_metadata["license"][0]["@type"] == "CreativeWork"
    assert dats_dataset.schema_org_metadata["license"][0]["name"] == "CC BY-ND"
    assert type(dats_dataset.schema_org_metadata["keywords"]) is list
    assert type(dats_dataset.schema_org_metadata["creator"]) is list
    assert dats_dataset.schema_org_metadata["creator"][0]["@type"] == "Organization"
    assert dats_dataset.schema_org_metadata["creator"][0]["name"] == "McGill Center for Integrative Neuroscience"


def test_jsonld_creator_person(new_dataset):
    """
    Change dats data: add creator person; remove creators
    """
    assert new_dataset.fspath == './test/test_dataset'
    dats_dataset = DATSDataset(datasetpath=new_dataset.fspath)
    assert type(dats_dataset.schema_org_metadata) is dict
    person_creator = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "test@example.org",
            "affiliations": [
                {"name": "University"},
                {"name": "University2"},
                {"name": "University3"},
                {"name": "University4"}
            ]
    }
    # change creators type to Person
    dats_dataset.descriptor["creators"] = [person_creator]
    assert dats_dataset.schema_org_metadata["creator"][0]["@type"] == "Person"
    assert dats_dataset.schema_org_metadata["creator"][0]["givenName"] == "Jane"
    assert dats_dataset.schema_org_metadata["creator"][0]["name"] == "Jane Doe"
    assert type(dats_dataset.schema_org_metadata["creator"][0]["affiliation"]) is list
    for org in dats_dataset.schema_org_metadata["creator"][0]["affiliation"]:
        assert org["@type"] == "Organization"
        assert org["name"] is not None
    # remove first name in person
    del person_creator["firstName"]
    assert dats_dataset.schema_org_metadata["creator"][0]["name"] == "Name is not provided"
    # mess up a bit to check for exception
    dats_dataset.descriptor["creators"] = None
    assert TypeError
    assert dats_dataset.schema_org_metadata is None
