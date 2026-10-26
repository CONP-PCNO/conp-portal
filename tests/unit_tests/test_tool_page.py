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


def test_container_info_registry_spellings_all_build_with_apptainer():
    # Docker Hub named by host: these 40 tools had no Alliance section
    for host in ("index.docker.io", "docker.io", "hub.docker.com", "index.docker.io/"):
        info = container_info({"image": "mcin/docker-fsl:latest", "index": host, "type": "docker"})
        assert info["pull"] == "docker://mcin/docker-fsl:latest"
        assert info["reference"] == "docker://mcin/docker-fsl:latest"
        assert info["hub_url"] == "https://hub.docker.com/r/mcin/docker-fsl"
        assert info["sif"] == "docker-fsl_latest.sif"
    # another registry, already in the image name
    ghcr = container_info({"image": "ghcr.io/rob-luke/app:v0.3.8", "index": "ghcr.io", "type": "docker"})
    assert ghcr["pull"] == "docker://ghcr.io/rob-luke/app:v0.3.8" and ghcr["hub_url"] is None
    # another registry, not in the image name
    quay = container_info({"image": "org/tool:1", "index": "quay.io", "type": "docker"})
    assert quay["pull"] == "docker://quay.io/org/tool:1"
    # "docker:<image>:<tag>" in the index carries the whole reference
    odd = container_info({"image": "elodiegermani/nguyen-etal-2021",
                          "index": "docker:elodiegermani/nguyen-etal-2021:latest", "type": "docker"})
    assert odd["pull"] == "docker://elodiegermani/nguyen-etal-2021:latest"
    # unchanged: docker:// and shub:// indexes, Singularity without an index
    assert container_info({"image": "a/b:1", "index": "docker://", "type": "docker"})["pull"] == "docker://a/b:1"
    assert container_info({"image": "c/d", "index": "shub://", "type": "singularity"})["pull"] == "shub://c/d"


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
    assert 'APPTAINER_TMPDIR=$SCRATCH/apptainer/tmp' in html   # not /tmp, which uses memory on login nodes
    assert 'href="https://docs.alliancecan.ca/wiki/Python#Creating_and_using_a_virtual_environment"' in html   # each step cites its source
    assert 'href="https://docs.alliancecan.ca/wiki/Running_jobs"' in html
    assert 'salloc --account' not in html         # compute nodes on some clusters have no internet: build on a login node
    assert 'Show 1 optional input' in html
    assert 'https://hub.docker.com/r/org/tool' in html


def test_tool_page_on_cbrain(app):
    html = _render(app, _pipeline(
        platforms=[{"img": "", "uri": "https://portal.cbrain.mcgill.ca/userfiles?prepare_tool_id=1"}],
        cbrain={"software": "Tool", "versions": ["1.0"], "tool": "T"}))
    assert 'Use on CBRAIN' in html
    assert 'CBRAIN runs Tool 1.0.' in html


def test_tool_page_cite_licence_and_job(app):
    html = _render(app, _pipeline(
        title='FreeSurfer-Recon-all', name='FreeSurfer-Recon-all', author='Martinos Center for Biomedical Imaging',
        publicationdate='2020-09-23', doi='10.5281/zenodo.4043546', **{'tool-version': 'v6.0.0'},
        description='Runs recon-all on a T1-weighted image.',
        inputs=[{'id': 'license', 'name': 'License file', 'type': 'File'},
                {'id': 'input', 'name': 'NIFTI file', 'type': 'File'}],
        **{'suggested-resources': {'cpu-cores': 1, 'ram': 10240, 'walltime-estimate': 960}}))
    # Cite: the descriptor's Zenodo record in three formats, with a note to cite the software too
    assert 'id="tp-cite"' in html and 'data-cite-format="bibtex"' in html
    assert 'Martinos Center for Biomedical Imaging (2020): FreeSurfer-Recon-all. V. 6.0.0. Zenodo. (software). https://doi.org/10.5281/zenodo.4043546' in html
    assert 'TY  - COMP' in html and 'Cite the software itself too' in html
    # Licence file: where to get FreeSurfer's, and which input takes it
    assert 'id="tp-licence"' in html and 'surfer.nmr.mgh.harvard.edu/registration.html' in html
    assert '<code>license</code> in <code>invocation.json</code>' in html
    # The 16-minute estimate is labelled as the authors' and recon-all as taking hours
    assert "the descriptor authors' estimate, not a measurement" in html
    assert 'a full recon-all run usually takes hours' in html
    # A complete job script, sized from the descriptor (10240 MB -> 10G), 12 h for recon-all
    assert '#SBATCH --time=12:00:00' in html and '#SBATCH --mem=10G' in html and '#SBATCH --cpus-per-task=1' in html


def test_docker_hub_links_are_lower_case():
    info = container_info({"image": "MontrealSergiy/BEst:latest", "index": "docker://", "type": "docker"})
    assert info["hub_url"] == "https://hub.docker.com/r/montrealsergiy/best"
