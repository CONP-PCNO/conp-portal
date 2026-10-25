"""Tests for the dataset landing page helpers and template (dataset.html)."""
import json
import pytest
from flask import render_template

from app.search.dataset_page import (
    citation_bibtex,
    citation_key,
    citation_ris,
    citation_text,
    clean_version,
    dataset_doi,
    dats_record_html,
    direct_download,
    publication_citations,
    title_html,
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
    assert clean_version("2024-08-01T21:15:15.153118") == "2024-08-01"


def test_citation_key():
    assert citation_key("projects/preventad-open", "2019") == "conp_preventad_open_2019"
    assert citation_key(None, None) == "conp_dataset"


def test_citation_text():
    text = citation_text(["A", "B", "C", "D"], "2020", "Title", "1.0", "https://n2t.net/ark:/1/x")
    assert text == "A; B; C; et al. (2020): Title. V. 1.0. CONP Portal. (dataset). https://n2t.net/ark:/1/x"
    assert citation_text(None, None, "T", None, None) == "T. CONP Portal. (dataset)."
    # DataCite form with a DOI: the DOI's publisher replaces the Portal and the ARK
    text = citation_text(["PERFORM Centre Concordia University"], "2019", "PERFORM Dataset; one control subject",
                         "1.0", "https://n2t.net/ark:/1/x", doi="10.5281/zenodo.3518486", publisher="Zenodo")
    assert text == ("PERFORM Centre Concordia University (2019): PERFORM Dataset; one control subject. "
                    "V. 1.0. Zenodo. (dataset). https://doi.org/10.5281/zenodo.3518486")
    assert "V. 2.1." in citation_text(["A"], "2009", "T", "v2.1", None)


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
    assert 'and the ability to include' in html
    assert 'Canadian dataset' in html            # conpStatus "Canadian"
    assert 'dp-views' in html and '1,234' in html
    assert 'cd demo' in html and 'datalad get .<span class="dp-comment">' in html
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


ZEN = {
    "identifier": {"identifier": "https://doi.org/10.5281/zenodo.10589601", "identifierSource": "DOI"},
    "title": "Paper is not enough",
    "dates": [{"date": "2024-01-31 17:09:34", "type": {"value": "date created"}}],
    "distributions": [{"formats": ["ZIP"], "size": 789.1, "unit": {"value": "MB"}, "access": {
        "landingPage": "https://zenodo.org/records/10589602",
        "accessURL": "https://zenodo.org/api/records/10589602/files/Dataset_x.zip/content",
        "authorizations": [{"value": "public"}]}}],
    "extraProperties": [{"category": "CONP_status", "values": [{"value": "Canadian"}]}],
}


def test_dataset_doi_and_doi_citation():
    assert dataset_doi(ZEN) == ("10.5281/zenodo.10589601", "Zenodo")
    assert dataset_doi({"identifier": {"identifier": "https://n2t.net/ark:/70798/x"}}) == (None, None)
    text = citation_text(["A", "B"], "2024", "T", None, "https://n2t.net/ark:/1/x",
                         doi="10.5281/zenodo.10589601", publisher="Zenodo")
    assert text == "A; B (2024): T. Zenodo. (dataset). https://doi.org/10.5281/zenodo.10589601"
    bib = citation_bibtex(["A"], "2024", "T", None, None, "projects/x", doi="10.5281/zenodo.1", publisher="Zenodo")
    assert "doi = {10.5281/zenodo.1}" in bib and "CONP Portal" not in bib
    ris = citation_ris(["A"], "2024", "T", None, None, doi="10.5281/zenodo.1", publisher="Zenodo")
    assert "DO  - 10.5281/zenodo.1" in ris and "PB  - Zenodo" in ris


def test_direct_download():
    d = direct_download(ZEN)
    assert d["host"] == "Zenodo" and d["format"] == "ZIP" and d["url"].endswith("/content")
    no_url = json.loads(json.dumps(ZEN))
    del no_url["distributions"][0]["access"]["accessURL"]
    assert direct_download(no_url)["url"] == "https://zenodo.org/api/records/10589602/files-archive"
    private = json.loads(json.dumps(ZEN))
    private["distributions"][0]["access"]["authorizations"] = [{"value": "private"}]
    assert direct_download(private) is None
    assert direct_download({"distributions": [{"access": {"landingPage": "https://example.org",
                                                          "authorizations": [{"value": "public"}]}}]}) is None
    osf = {"distributions": [{"access": {"landingPage": "https://osf.io/q482e",
                                         "accessURL": "https://files.us.osf.io/v1/resources/znt9d/providers/osfstorage/?zip=q482e",
                                         "authorizations": [{"value": "public"}]}}]}
    assert direct_download(osf)["host"] == "OSF" and direct_download(osf)["format"] == "ZIP"


def test_publication_citations():
    pubs = publication_citations({"primaryPublications": [
        {"title": "BigBrain: an ultrahigh-resolution 3D human brain model", "publicationVenue": "Science",
         "authorsList": "Amunts, Katrin, et al."},
        {"title": "Second.", "authors": [{"fullName": "Jane Doe"}, {"firstName": "J", "lastName": "Roe"}],
         "dates": [{"date": "2021-03-01"}], "identifier": {"identifier": "https://doi.org/10.1000/xyz"}},
    ]})
    assert pubs[0]["text"] == "Amunts, Katrin, et al.. BigBrain: an ultrahigh-resolution 3D human brain model. Science." \
        or pubs[0]["text"].startswith("Amunts, Katrin, et al. BigBrain")
    assert pubs[0]["doi"] is None and "TY  - JOUR" in pubs[0]["ris"]
    assert pubs[1]["text"] == "Jane Doe, J Roe (2021). Second. https://doi.org/10.1000/xyz"
    assert "doi = {10.1000/xyz}" in pubs[1]["bibtex"] and pubs[1]["bibtex"].startswith("@article{doe_2021_2,")
    assert publication_citations({}) == []


def test_dats_record_html_escapes():
    html = str(dats_record_html({"title": "<b>x</b>", "keywords": [{"value": "a"}, {"value": "b"}],
                                 "extraProperties": [{"category": "CONP_status", "values": [{"value": "Canadian"}]}]}))
    assert "&lt;b&gt;x&lt;/b&gt;" in html
    assert "a, b" in html and "CONP status" in html
    # Plain names only (no raw DATS keys); the definition is in a tooltip.
    assert "extraProperties" not in html and "dp-dats-key" not in html
    assert 'class="dp-term"' in html and 'role="tooltip"' in html


def test_dats_record_html_flattens_nesting_and_drops_noise():
    """
    GIVEN a distribution with nested access, an empty description and @type
    THEN nested fields come out as one level of name/value lines, the size
         carries its unit, and empty fields and @type are left out
    """
    html = str(dats_record_html({
        "distributions": [{"formats": ["EDF", "JSON"], "size": 9.2, "unit": {"value": "GB"},
                           "access": {"landingPage": "https://eegnet.loris.ca",
                                      "authorizations": [{"value": "registered"}]}}],
        "spatialCoverage": [{"name": "North America", "description": ""}],
        "licenses": [{"@type": "License", "name": "CC-BY", "version": "4.0"}],
    }))
    assert "9.2 GB" in html and "EDF, JSON" in html
    assert "Landing page" in html and "Authorizations" in html and ">Access<" not in html
    assert "Description" not in html and "@type" not in html and "License<" not in html
    # One block of lines (the distribution); single values and named things read as one line.
    assert html.count('class="dp-dats-sub"') == 1 and "dp-dats-item" not in html
    assert ">North America<" in html.replace('<div class="dp-dats-line">', '>') and "Name" not in html
    assert 'CC-BY <span class="dp-dats-note">· 4.0</span>' in html
    assert "The technical format of the dataset distribution" in html  # from the CONP DATS field guide


def test_dats_record_html_people_and_dates_read_as_lines():
    html = str(dats_record_html({
        "creators": [{"name": "McGill University"},
                     {"name": "Philippe Albouy", "roles": [{"value": "Principal Investigator"}]}],
        "dates": [{"date": "2019-10-31 00:00:00", "type": {"value": "start date"}}],
    }))
    assert 'Philippe Albouy <span class="dp-dats-note">· Principal Investigator</span>' in html
    assert '2019-10-31 <span class="dp-dats-note">· start date</span>' in html and "00:00:00" not in html


def test_dats_field_definitions_cover_the_top_level_labels():
    """Every top-level field the record names has a definition."""
    from app.search.dataset_page import _DATS_LABELS, dats_field_definitions
    defs = dats_field_definitions()
    top = ['title', 'description', 'creators', 'types', 'version', 'licenses', 'keywords', 'distributions',
           'privacy', 'isAbout', 'primaryPublications', 'spatialCoverage', 'dates', 'identifier', 'acknowledges']
    missing = [k for k in top if k not in defs]
    assert not missing, missing
    assert all(k in _DATS_LABELS for k in top)


def test_dataset_page_cite_and_dats(app):
    data = _data()
    with app.test_request_context('/dataset?id=projects/demo'):
        page = {"licences": [], "citation": "C.", "cbrainPipelinesUrl": "/p", "views": 0,
                "publications": publication_citations({"primaryPublications": [{"title": "P", "publicationVenue": "J"}]}),
                "direct_download": direct_download(ZEN), "dats_html": dats_record_html(ZEN), "doi": "10.5281/zenodo.10589601",
                "parents": [{"url": "/dataset?id=projects/parent", "title": "Parent dataset"}]}
        html = render_template('dataset.html', title='t', data=data, metadata=_metadata(), readme='',
                               page=page, ciBadgeUrl='', user=None)
    assert 'The publication describing it' in html and 'dp-pub1-bibtex' in html
    assert 'Show the full metadata record (DATS)' in html and 'class="dp-term"' in html
    assert 'in a single ZIP file' in html and 'Zenodo record' in html and 'tar.gz' not in html
    assert 'derived from' in html and 'Parent dataset' in html
    assert 'Also listed on the CONP Portal' in html


def test_title_html_sub_sup_only():
    html = str(title_html('T<sub>1</sub> <script>x</script>'))
    assert html == 'T<sub>1</sub> &lt;script&gt;x&lt;/script&gt;'


def test_modality_links_are_lower_case(app):
    html = _render(app, _data(modalities=["PET", "MRI"]), _metadata())
    assert 'search?modalities=pet' in html and 'search?modalities=mri' in html


def test_search_page_shows_30_per_page_by_default(app):
    with app.test_client() as client:
        html = client.get('/search').get_data(as_text=True)
        assert '"max_per_page": "30"' in html and '"limit": "30"' in html
        html = client.get('/search?max_per_page=10').get_data(as_text=True)
        assert '"max_per_page": "10"' in html


def test_direct_download_only_for_crawled_datasets(tmp_path):
    assert direct_download(ZEN, str(tmp_path)) is None          # no crawler marker
    (tmp_path / '.conp-zenodo-crawler.json').write_text('{}')
    assert direct_download(ZEN, str(tmp_path))['host'] == 'Zenodo'


def test_authorizations_does_not_empty_the_record(tmp_path):
    from app.search.models import DATSDataset
    d = tmp_path / 'conp-dataset' / 'projects' / 'demo'
    d.mkdir(parents=True)
    (d / 'DATS.json').write_text(json.dumps(ZEN))
    dats = DATSDataset(str(d))
    assert dats.authorizations == 'public'
    assert dats.authorizations == 'public'                      # was "None" the second time
    assert direct_download(dats.descriptor)['host'] == 'Zenodo'


def test_ark_is_prominent_and_copyable(app):
    html = _render(app, _data(), _metadata())
    assert 'class="dp-ark-link" href="https://n2t.net/ark:/1/x"' in html
    assert 'data-copy-target="dp-ark-url"' in html and 'data-copy-target="dp-ark-meta"' in html
    # the ARK row is the first one under All metadata
    meta = html[html.index('id="metadata"'):]
    assert meta.index('ARK identifier') < meta.index('Creators')


def test_licence_chip_links_to_licence_row(app):
    html = _render(app, _data(), _metadata(licenses=["Refer to Brain-CODE Governance Policy"]))
    assert 'href="#dp-licence"' in html and 'id="dp-licence"' in html
    chip = html[html.index('href="#dp-licence"') - 40:html.index('href="#dp-licence"') + 120]
    assert 'target="_blank"' not in chip                       # stays on the page
    html = _render(app, _data(), _metadata(licenses=["CC0"]))
    assert 'creativecommons.org/publicdomain/zero' in html or 'href="#dp-licence"' not in html


def test_datalad_comment_is_separate_from_the_command(app):
    html = _render(app, _data(), _metadata())
    assert 'datalad get .<span class="dp-comment">   # all files; or give individual paths</span>' in html
    assert 'datalad get *' not in html
