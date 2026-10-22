"""
Tests for dataset logos given in app/static/datasets/dataset-logos.json, used
when a dataset's own DATS.json has no logo.
"""
import json
import os

from app.dats import (
    DATASET_LOGOS_JSON,
    DEFAULT_LOGO,
    dataset_logo_override,
    load_dataset_logos,
    resolve_dataset_logo,
)
from app.models import Dataset
from app.search.models import DATSDataset

IMG_ID = "projects/PiDose"                            # an "img" entry
URL_ID = "projects/Participant_level_contrast_maps"   # a "url" entry
UNKNOWN_ID = "projects/no-such-dataset"


def _make_dataset(tmp_path, logo=None, name="ds", files=()):
    """A dataset folder whose DATS.json has a logo (if given) or none, plus
    the (empty) files listed in files."""
    path = tmp_path / name
    path.mkdir(parents=True)
    for f in files:
        (path / f).write_bytes(b"img")
    extra = [{"category": "subjects", "values": [{"value": "1"}]}]
    if logo:
        extra.insert(0, {"category": "logo", "values": [{"value": logo}]})
    (path / "DATS.json").write_text(json.dumps({"title": name, "extraProperties": extra}))
    return str(path)


def test_dataset_logos_data_is_consistent():
    """
    GIVEN dataset-logos.json
    THEN every entry has exactly one of img/url, a label, a source, a reason and
         a tier, and every img file exists
    """
    with open(DATASET_LOGOS_JSON) as f:
        logos = json.load(f)["datasets"]
    assert logos, "no dataset logos are listed"
    for dataset_id, entry in logos.items():
        assert dataset_id.startswith("projects/"), dataset_id
        assert bool(entry.get("img")) != bool(entry.get("url")), dataset_id
        for key in ("label", "source", "why"):
            assert entry.get(key), f"{dataset_id}: no {key}"
        assert entry.get("tier") in ("A", "B", "C"), dataset_id
        if entry.get("img"):
            assert os.path.isfile(os.path.join("app/static", entry["img"])), entry["img"]
        else:
            assert entry["url"].startswith("https://"), dataset_id


def test_dataset_without_dats_logo_gets_override(tmp_path):
    """
    GIVEN a dataset whose DATS.json has no logo and which is listed in
          dataset-logos.json
    THEN LogoFilepath is the listed image (or URL)
    """
    logos = load_dataset_logos()
    dats = DATSDataset(_make_dataset(tmp_path), dataset_id=IMG_ID)
    assert dats.OwnLogoFilepath is None
    assert dats.LogoFilepath == os.path.join("app/static", logos[IMG_ID]["img"])
    assert os.path.isfile(dats.LogoFilepath)

    dats = DATSDataset(_make_dataset(tmp_path, name="ds2"), dataset_id=URL_ID)
    assert dats.LogoFilepath == logos[URL_ID]["url"]


def test_dataset_with_dats_logo_keeps_its_own(tmp_path):
    """
    GIVEN a dataset listed in dataset-logos.json whose DATS.json has a logo
    THEN its own logo wins, whether a file or a URL
    """
    path = _make_dataset(tmp_path, logo="logo.png", files=["logo.png"])
    dats = DATSDataset(path, dataset_id=IMG_ID)
    assert dats.LogoFilepath == os.path.join(path, "logo.png")
    # Reading it again gives the same answer (the old code pop()ed the value).
    assert dats.LogoFilepath == os.path.join(path, "logo.png")

    url = "https://example.org/own-logo.png"
    dats = DATSDataset(_make_dataset(tmp_path, logo=url, name="ds2"), dataset_id=URL_ID)
    assert dats.LogoFilepath == url


def test_logo_file_in_dataset_folder_wins_over_override(tmp_path):
    """
    GIVEN a dataset listed in dataset-logos.json whose DATS.json names no logo
          but whose folder holds a logo file next to DATS.json and README.md
    THEN that file is used (any common image extension, any case)
    """
    path = _make_dataset(tmp_path, files=["README.md", "Logo.PNG"])
    dats = DATSDataset(path, dataset_id=IMG_ID)
    assert dats.OwnLogoFilepath == os.path.join(path, "Logo.PNG")
    assert dats.LogoFilepath == os.path.join(path, "Logo.PNG")

    # Files that merely contain "logo" are not taken.
    path = _make_dataset(tmp_path, name="ds2", files=["logo_old.png", "lab-logo.jpg"])
    assert DATSDataset(path, dataset_id=IMG_ID).OwnLogoFilepath is None


def test_dats_logo_that_is_missing_falls_back(tmp_path):
    """
    GIVEN a DATS.json naming a logo file that is not in the dataset folder
    THEN a logo file that is there is used, else the override
    """
    path = _make_dataset(tmp_path, logo="images/logo.png", files=["logo.jpg"])
    assert DATSDataset(path, dataset_id=IMG_ID).LogoFilepath == os.path.join(path, "logo.jpg")

    path = _make_dataset(tmp_path, logo="images/logo.png", name="ds2")
    assert DATSDataset(path, dataset_id=IMG_ID).LogoFilepath == dataset_logo_override(IMG_ID)


def test_unknown_dataset_gets_default(tmp_path):
    """
    GIVEN a dataset with no DATS logo that is not in dataset-logos.json
    THEN LogoFilepath is the default image
    """
    assert DATSDataset(_make_dataset(tmp_path), dataset_id=UNKNOWN_ID).LogoFilepath == DEFAULT_LOGO
    assert DATSDataset(_make_dataset(tmp_path, name="ds2")).LogoFilepath == DEFAULT_LOGO
    assert dataset_logo_override(UNKNOWN_ID) is None
    assert dataset_logo_override(None) is None


def test_dataset_id_is_derived_from_path(tmp_path):
    """
    GIVEN a dataset folder under conp-dataset/projects/ and no explicit id
    THEN its Portal id is derived from the path and the override applies
    """
    path = _make_dataset(tmp_path, name="conp-dataset/projects/PiDose")
    dats = DATSDataset(path)
    assert dats.dataset_id == IMG_ID
    assert dats.LogoFilepath == dataset_logo_override(IMG_ID)


def test_resolve_dataset_logo_for_index_values():
    """
    GIVEN the logo value stored in the search index
    THEN the default image (or nothing) is replaced by the override, and any
         other value is kept
    """
    override = dataset_logo_override(IMG_ID)
    assert resolve_dataset_logo(IMG_ID, DEFAULT_LOGO) == override
    assert resolve_dataset_logo(IMG_ID, None) == override
    assert resolve_dataset_logo(IMG_ID, "/data/x/logo.png") == "/data/x/logo.png"
    assert resolve_dataset_logo(UNKNOWN_ID, DEFAULT_LOGO) == DEFAULT_LOGO


def test_dataset_logo_route_serves_override(session, test_client, tmp_path):
    """
    GIVEN calling the route "/dataset_logo" for datasets with no DATS logo
    THEN an "img" override is served from app/static, and a "url" override
         redirects to that URL
    """
    logos = load_dataset_logos()
    session.add(Dataset(dataset_id=IMG_ID, name="PiDose", version="1.0", is_private=False,
                        fspath=_make_dataset(tmp_path, name="img")))
    session.add(Dataset(dataset_id=URL_ID, name="Contrast maps", version="1.0", is_private=False,
                        fspath=_make_dataset(tmp_path, name="url")))
    # flush, not commit: the rows must not outlive this test (other tests
    # list every dataset in the database)
    session.flush()

    res = test_client.get("/dataset_logo", query_string={"id": IMG_ID})
    assert res.status_code == 200
    with open(os.path.join("app/static", logos[IMG_ID]["img"]), "rb") as f:
        assert res.data == f.read()

    res = test_client.get("/dataset_logo", query_string={"id": URL_ID})
    assert res.status_code == 302
    assert res.headers["Location"] == logos[URL_ID]["url"]


def test_dataset_logo_route_serves_generic_icon(session, test_client, tmp_path):
    """
    GIVEN a dataset with no logo of its own and no override
    THEN "/dataset_logo" serves the CONP generic dataset icon (an SVG)
    """
    session.add(Dataset(dataset_id=UNKNOWN_ID, name="No logo", version="1.0", is_private=False,
                        fspath=_make_dataset(tmp_path, name="nologo")))
    session.flush()
    res = test_client.get("/dataset_logo", query_string={"id": UNKNOWN_ID})
    assert res.status_code == 200 and res.mimetype == "image/svg+xml"
    assert DEFAULT_LOGO.endswith("img/datasets/default.svg") and os.path.isfile(DEFAULT_LOGO)
