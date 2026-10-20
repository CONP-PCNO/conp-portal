"""Tests for the tool page helpers and template (pipeline.html)."""
from flask import render_template

from app.pipelines.tool_page import (
    container_info,
    resources_text,
    split_inputs,
    tag_list,
    tool_page_context,
)


def test_tag_list():
    assert tag_list({"domain": ["neuroinformatics", "fMRI"]}) == ["neuroinformatics", "fMRI"]
    assert tag_list("Boutiques") == []
    assert tag_list("mri, Boutiques, MRI") == ["mri"]
    assert tag_list(None) == []


def test_container_info_docker_hub():
    info = container_info({"image": "freesurfer/freesurfer:8.2.0", "index": "docker://", "type": "singularity"})
    assert info["reference"] == "docker://freesurfer/freesurfer:8.2.0"
    assert info["hub_url"] == "https://hub.docker.com/r/freesurfer/freesurfer"
    assert info["pull"] == "docker://freesurfer/freesurfer:8.2.0"
    assert info["sif"] == "freesurfer_8.2.0.sif"


def test_container_info_official_and_other_registry():
    assert container_info({"image": "ubuntu:22.04", "type": "docker"})["hub_url"] == "https://hub.docker.com/_/ubuntu"
    quay = container_info({"image": "quay.io/org/tool:1", "index": "docker://", "type": "docker"})
    assert quay["hub_url"] is None and quay["pull"] == "docker://quay.io/org/tool:1"
    assert container_info({}) is None
    assert container_info(None) is None


def test_resources_text():
    assert resources_text({"cpu-cores": 4, "ram": 16384, "walltime-estimate": 1440}) == \
        "4 cores, 16 GB memory, walltime estimate about 24 min"
    assert resources_text({"ram": 8, "walltime-estimate": 7200}) == "8 GB memory, walltime estimate about 2 h"
    assert resources_text({"cpu-cores": 1}) == "1 core"
    assert resources_text({}) is None
    assert resources_text(None) is None


def test_split_inputs_required_first():
    required, optional = split_inputs([
        {"id": "a", "optional": True}, {"id": "b", "optional": False}, {"id": "c"},
    ])
    assert [i["id"] for i in required] == ["b", "c"]
    assert [i["id"] for i in optional] == ["a"]


def _pipeline(**over):
    p = {
        "id": "zenodo.123", "title": "Tool_v1", "author": "Lab", "description": "Does things.",
        "publicationdate": "2026-01-01", "doi": "10.5281/zenodo.123", "downloads": 3,
        "tags": {"domain": ["mri"]}, "icon": {"src": "/static/img/tools/x.png", "label": "X"},
        "container-image": {"image": "org/tool:1", "index": "docker://", "type": "docker"},
        "suggested-resources": {"cpu-cores": 2}, "tool-version": "1", "schema-version": "0.5",
        "inputs": [{"id": "in", "name": "Input", "type": "File", "optional": False, "description": "The input."},
                   {"id": "opt", "name": "Flag", "type": "Flag", "optional": True}],
        "output-files": [{"id": "out", "name": "Output", "path-template": "[OUT]"}],
        "platforms": [{"img": "", "uri": ""}], "cbrain": None,
        "ark_id": "https://n2t.net/ark:/1/p",
    }
    p.update(over)
    return p


def _render(app, pipeline):
    with app.test_request_context('/pipeline?id=' + pipeline["id"]):
        return render_template('pipeline.html', title='t', pipeline=pipeline,
                               page=tool_page_context(pipeline))


def test_tool_page_not_on_cbrain(app):
    html = _render(app, _pipeline())
    assert 'class="tp-title">Tool_v1<' in html
    assert 'On CBRAIN' not in html
    assert 'bosh exec launch -s zenodo.123 invocation.json -v /data:/data' in html
    assert 'apptainer build tool_1.sif docker://org/tool:1' in html
    assert 'pip install boutiques' in html
    assert '--user' not in html                   # Alliance docs warn against pip install --user
    assert 'virtualenv --no-download ~/boutiques-env' in html
    assert 'bosh pull zenodo.123' in html
    assert 'cd $SCRATCH/conp' in html             # never build into an unwritable working directory
    assert html.index('salloc --account') < html.index('apptainer build')   # build in a job, not on a login node
    assert 'APPTAINER_CACHEDIR=${SLURM_TMPDIR:?not in the job yet}/apptainer' in html   # stops outside a job
    assert 'salloc --account=' in html
    assert 'Show 1 optional input' in html
    assert 'https://hub.docker.com/r/org/tool' in html


def test_tool_page_on_cbrain(app):
    html = _render(app, _pipeline(
        platforms=[{"img": "", "uri": "https://portal.cbrain.mcgill.ca/userfiles?prepare_tool_id=1"}],
        cbrain={"software": "Tool", "versions": ["1.0"], "tool": "T"}))
    assert 'Use on CBRAIN' in html
    assert 'CBRAIN runs Tool 1.0.' in html
