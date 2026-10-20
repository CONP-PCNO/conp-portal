"""Tests for the dataset landing page helpers and template (dataset.html)."""
import pytest
from flask import render_template

from app.search.dataset_page import (
    citation_bibtex,
    citation_key,
    citation_ris,
    citation_text,
    clean_version,
    licence_badges,
    short_licence,
    strip_title_heading,
)


@pytest.mark.parametrize("name,label,url", [
    ("CC BY-SA", "CC BY-SA", None),
    ("cc-zero", "CC0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    ("CC0 1.0 Universal", "CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    ("Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License",
     "CC BY-NC-SA 4.0", "https://creativecommons.org/licenses/by-nc-sa/4.0/"),
    ("CC-BY-4.0", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    ("CC-By Attribution 4.0 International", "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    ("cc-by-nd-4.0", "CC BY-ND 4.0", "https://creativecommons.org/licenses/by-nd/4.0/"),
    ('{"id": "cc-by-4.0"}', "CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    ("ODbL", "ODbL", "https://opendatacommons.org/licenses/odbl/"),
    ("PDDL", "PDDL", "https://opendatacommons.org/licenses/pddl/"),
    ("MIT License", "MIT", "https://opensource.org/license/mit"),
    ("Refer to Brain-CODE Governance Policy", "Data use terms", None),
    ("https://alleninstitute.org/legal/terms-use/", "Data use terms",
     "https://alleninstitute.org/legal/terms-use/"),
])
def test_short_licence(name, label, url):
    badge = short_licence(name)
    assert badge["label"] == label
    assert badge["url"] == url
    assert badge["full"]


def test_short_licence_none():
    assert short_licence(None) is None
    assert short_licence("None") is None
    assert licence_badges(None) == []


def test_licence_badges_deduplicates():
    badges = licence_badges(["CC BY-SA", "CC BY-SA", "PDDL"])
    assert [b["label"] for b in badges] == ["CC BY-SA", "PDDL"]


def test_strip_title_heading():
    html = '<h1>My Dataset</h1>\n<p>Body</p>'
    assert strip_title_heading(html, "My dataset").strip() == "<p>Body</p>"
    other = '<h1>Something else</h1><p>Body</p>'
    assert strip_title_heading(other, "My dataset") == other
    assert strip_title_heading(("Readme Not Found", 404), "x") == ""


def test_citation_bibtex():
    bib = citation_bibtex(["BigBrain project", "Alan C. Evans"], "2020", "Volumes & 50% more", "1.0",
                          "https://n2t.net/ark:/1/x", "projects/BigBrain_3DClassifiedVolumes")
    assert bib.startswith("@misc{conp_BigBrain_3DClassifiedVolumes_2020,\n")
    assert "author = {{BigBrain project} and Alan C. Evans}" in bib
    assert "title = {{Volumes \\& 50\\% more}}" in bib
    assert "url = {https://n2t.net/ark:/1/x}" in bib
    assert bib.endswith("\n}")
    assert "author" not in citation_bibtex(None, None, "T", None, None)


def test_citation_ris():
    ris = citation_ris(["A B", "C D"], "2021", "Title", "2", "https://n2t.net/ark:/1/x").split("\n")
    assert ris[0] == "TY  - DATA"
    assert ris[1:3] == ["AU  - A B", "AU  - C D"]
    assert "PY  - 2021" in ris and "ET  - 2" in ris and "UR  - https://n2t.net/ark:/1/x" in ris
    assert ris[-1] == "ER  - "


def test_clean_version():
    assert clean_version("1.0") == "1.0"
    assert clean_version("None") is None
    assert clean_version(None) is None
    assert clean_version(" ") is None


def test_citation_key():
    assert citation_key("projects/preventad-open", "2019") == "conp_preventad_open_2019"
    assert citation_key(None, None) == "conp_dataset"


def test_citation_text():
    text = citation_text(["A", "B", "C", "D"], "2020", "Title", "1.0", "https://n2t.net/ark:/1/x")
    assert text == "A, B, C, et al. (2020). Title, version 1.0. CONP Portal. https://n2t.net/ark:/1/x"
    assert citation_text(None, None, "T", None, None) == "T. CONP Portal."


def _data(**over):
    data = {
        "id": "projects/demo", "name": "demo", "title": "Demo dataset", "ark_id": "https://n2t.net/ark:/1/x",
        "creators": ["Lab"], "origin": "", "size": "1.0 GB", "files": 3, "subjects": 1,
        "formats": ["NIfTI"], "modalities": ["MRI"], "licenses": ["CC0"], "version": "1.0",
        "authorizations": "public", "registrationPage": None, "downloadOptions": None,
        "logoFilepath": "", "thumbnailURL": "/dataset_logo?id=projects/demo", "cbrain_id": "",
        "showDownloadButton": True, "zipLocation": "/data/demo.tar.gz", "evidencePublication": None,
        "evidencePublicationType": None, "dateAdded": "2020-01-01", "dateUpdated": "2021-01-01",
        "primaryPublications": None, "principalInvestigators": None, "status": "Working",
        "conpStatus": "Canadian",
    }
    data.update(over)
    return data


def _metadata(**over):
    meta = {
        "schema_org_metadata": {}, "description": "A short description.", "contact": None,
        "licenses": ["CC0"], "sources": "https://example.org", "keywords": ["brain"],
        "parentDatasets": None, "primaryPublications": None, "childDatasets": [],
        "dimensions": None, "producedBy": None, "isAbout": None, "acknowledges": None,
        "spatialCoverage": None, "dates": None, "remoteUrl": None, "registrationPage": None,
        "downloadOptions": None, "registrationEmail": False,
    }
    meta.update(over)
    return meta


def _render(app, data, metadata):
    page = {"licences": licence_badges(metadata["licenses"]), "citation": "C.", "cbrainPipelinesUrl": "/pipeline-search", "views": 1234}
    with app.test_request_context('/dataset?id=' + data["id"]):
        return render_template('dataset.html', title='t', data=data, metadata=metadata,
                               readme='<p>Readme</p>', page=page, ciBadgeUrl='', user=None)


def test_dataset_page_open_dataset(app):
    html = _render(app, _data(), _metadata())
    assert 'class="dp-title">Demo dataset<' in html
    assert 'data-dp-download' in html            # direct download offered
    assert 'datalad install demo' in html
    assert 'version 1.0, added 2020-01-01, updated 2021-01-01' in html
    assert 'in a single tar.gz file' in html
    assert 'Canadian dataset' in html            # conpStatus "Canadian"
    assert 'dp-views' in html and '1,234' in html
    assert 'cd demo' in html and 'datalad get *' in html
    assert 'Open in' not in html                  # no CBRAIN id: no CBRAIN row
    assert 'Request access' not in html
    assert html.index('aria-controls="metadata"') < html.index('aria-controls="cite"')


def test_dataset_page_registered_offsite(app):
    html = _render(app, _data(showDownloadButton=False, authorizations="registered"),
                   _metadata(downloadOptions="offsite", registrationPage="https://reg.example.org/"))
    assert 'Request access' in html
    assert 'Go to the source' in html
    assert 'data-dp-download' not in html
    assert 'datalad install' not in html
