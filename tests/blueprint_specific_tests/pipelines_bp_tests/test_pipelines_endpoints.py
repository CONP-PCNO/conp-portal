"""
Unit tests for endpoints in the pipelines blueprint
"""
from app import cli


def test_pipelines_route(test_client):
    """
    GIVEN calling the route "/pipelines"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/pipelines")
    assert res.status_code == 200


def test_pipeline_search_route(session, new_pipeline, test_client, app, runner):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN no user is logged in
    AND no filter is used
    THEN should return success code and all pipelines
    """

    session.add(new_pipeline)
    session.commit()

    cli.register(app)
    result = runner.invoke(args=["update_pipeline_data"])

    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/pipeline-search", headers = headers)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert body is not None
    assert body["authorized"] == False
    assert body["elements"] is not None
    assert body["total"] > 0

def test_pipeline_search_route_with_filter(session, new_pipeline, test_client):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN no user is logged in
    AND a filter is used
    THEN should return success code and filtered pipelines
    """

    session.add(new_pipeline)
    session.commit()

    query = {'search': 'RandomSearchTerm'}
    headers = {'Content-Type': 'application/json'}
    res = test_client.get("/pipeline-search", headers = headers, query_string = query)
    assert res.status_code == 200

    body = res.get_json(force=True)

    assert body is not None
    assert body["authorized"] == False
    assert body["elements"] is not None
    assert body["total"] == 0


def test_share_route(test_client):
    """
    GIVEN calling the route "/share"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/share")
    assert res.status_code == 200

def test_tools_route(test_client):
    """
    GIVEN calling the route "/tools"
    WHEN no user is logged in
    THEN should return success code
    """
    res = test_client.get("/tools")
    assert res.status_code == 200


TOOL_ICONS_JSON = "app/static/pipelines/tool-icons.json"


def _tool_icons_data():
    import json
    with open(TOOL_ICONS_JSON) as f:
        return json.load(f)


def _fake_pipelines(mapped_id, unmapped_id):
    return [
        {"ID": mapped_id, "TITLE": "Mapped tool", "DOWNLOADS": 2,
         "PUBLICATIONDATE": "2020-01-01", "tags": {"domain": ["mri"]}},
        {"ID": unmapped_id, "TITLE": "Unmapped tool", "DOWNLOADS": 1,
         "PUBLICATIONDATE": "2020-01-01", "tags": {"domain": ["mri"]}},
    ]


def test_tool_icons_data_is_consistent():
    """
    GIVEN tool-icons.json
    THEN every mapped tool points to a known family, every family has a
         label, a source and an image file that exists, and the generic
         "default" icon is complete and its SVG and PNG fallback exist
    """
    import os
    data = _tool_icons_data()
    families = data["families"]
    assert data["pipelines"], "no tools are mapped"
    for zenodo_id, family in data["pipelines"].items():
        assert zenodo_id.startswith("zenodo."), zenodo_id
        assert family in families, f"{zenodo_id} -> unknown family {family}"
    for family, info in families.items():
        assert info.get("label"), family
        assert info.get("source"), family
        assert os.path.isfile(os.path.join("app/static", info["img"])), info["img"]
    default = data["default"]
    assert default["label"] == "Tool"
    assert default.get("source") and default.get("why")
    for key in ("img", "fallback_img"):
        assert os.path.isfile(os.path.join("app/static", default[key])), default[key]


def test_get_tool_icons(app):
    """
    GIVEN get_tool_icons() and tool_icon()
    THEN a mapped id gets the static URL of its family's image and its label,
         an unmapped id gets the generic CONP icon, and no id gets None
    """
    from app.pipelines.routes import get_tool_icons, tool_icon
    data = _tool_icons_data()
    zenodo_id, family = next(iter(data["pipelines"].items()))
    with app.test_request_context():
        icons, default_icon = get_tool_icons()
    assert icons[zenodo_id]["label"] == data["families"][family]["label"]
    assert icons[zenodo_id]["src"].endswith("/static/" + data["families"][family]["img"])
    assert "generic" not in icons[zenodo_id]
    assert "zenodo.0" not in icons

    assert default_icon == {
        "src": default_icon["src"], "label": "Tool", "generic": True}
    assert default_icon["src"].endswith("/static/" + data["default"]["img"])

    assert tool_icon(zenodo_id, icons, default_icon) == icons[zenodo_id]
    assert tool_icon("zenodo.0", icons, default_icon) == default_icon
    for zid in list(data["pipelines"]) + ["zenodo.0", None]:
        assert tool_icon(zid, icons, default_icon) is not None


def test_get_tool_icons_without_default(app, monkeypatch, tmp_path):
    """
    GIVEN a tool-icons.json without a "default" entry
    THEN unmapped tools get None (the card then shows the old grey cog)
    """
    import json
    import os
    from app.pipelines.routes import get_tool_icons, tool_icon
    data = _tool_icons_data()
    del data["default"]
    (tmp_path / "app/static/pipelines").mkdir(parents=True)
    (tmp_path / TOOL_ICONS_JSON).write_text(json.dumps(data))
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))
    with app.test_request_context():
        icons, default_icon = get_tool_icons()
    assert default_icon is None
    assert tool_icon("zenodo.0", icons, default_icon) is None


def test_pipeline_search_returns_icon(monkeypatch, test_client):
    """
    GIVEN calling the route "/pipeline-search"
    WHEN one listed tool is mapped in tool-icons.json and one is not
    THEN the mapped tool carries its family icon (src + label) and the other
         carries the generic CONP icon; no element has icon None
    """
    from app.pipelines import pipelines as pipelines_utils
    data = _tool_icons_data()
    mapped_id, family = next(iter(data["pipelines"].items()))
    unmapped_id = "zenodo.0"
    monkeypatch.setattr(pipelines_utils, "get_pipelines_from_cache",
                        lambda search_query=None: _fake_pipelines(mapped_id, unmapped_id))

    res = test_client.get("/pipeline-search")
    assert res.status_code == 200
    elements = {e["id"]: e for e in res.get_json(force=True)["elements"]}

    assert elements[mapped_id]["icon"]["label"] == data["families"][family]["label"]
    assert elements[mapped_id]["icon"]["src"].endswith(data["families"][family]["img"])
    assert not elements[mapped_id]["icon"].get("generic")
    assert elements[unmapped_id]["icon"]["label"] == "Tool"
    assert elements[unmapped_id]["icon"]["generic"] is True
    assert elements[unmapped_id]["icon"]["src"].endswith(data["default"]["img"])
    assert all(e["icon"] is not None for e in elements.values())
