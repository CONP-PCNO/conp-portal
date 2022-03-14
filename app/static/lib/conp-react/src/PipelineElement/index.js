import React from "react";
import PropTypes from "prop-types";

import ViewsIcon from "../social/ViewsIcon"
import DownloadsIcon from "../social/DownloadsIcon"

const PipelineElement = props => {
  const { authorized, ...element } = props;
  const updateSelect = (event) => {
    props.updateActiveCbrainId(props.id, event.target.value)
  }
  const openPipeline = () => {
    if (props.activeCbrainId !== "") {
      window.open(props.activeCbrainId);
    }
  }

  const openModal = (pipelineUrl) => {
    if (props.activeCbrainId !== "") {
      $("#cbrainModal").modal("show");
      $("#btnCbrainLoaded").attr("href", pipelineUrl);
      $("#btnCbrainLoaded").on("click", function (event) {
        $("#cbrainModal").modal("hide");
      });
    }
  }

  const platforms = element.platforms.map((item, key) =>
    item.uri ?
      <div className="col">
        <span key={key} data-toggle="tooltip" title="Run Pipeline" style={{ maxWidth: "140px" }}>
          <a target="_blank" rel="noreferrer" className="btn" href={props.activeCbrainId === "" ? item.uri : props.activeCbrainId} onClick={() => openModal(item.uri)}>
            <img className="img-fluid" alt="Online platform" src={item.img} />
          </a>
        </span>
        <div className="dropdown">
          <button
              className="btn btn-outline-secondary dropdown-toggle m-1"
              type="button"
              id={"dropdown" + element.id}
              data-toggle="dropdown"
              data-display="static"
              aria-expanded="false"
              aria-label="pipeline">
            Dataset:
          </button>
          <ul className="dropdown-menu dropdown-menu-right" aria-labelledby={"dropdown" + element.id}>
            <li>
              <div className="form-check dropdown-item">
                <input className="form-check-input" type="radio" name={"datasets" + element.id} id="nonechoice" onChange={updateSelect} value="" checked={props.activeCbrainId === "" ? "checked" : null } />
                <label className="form-check-label" htmlFor="nonechoice">None</label>
              </div>
            </li>
            {props.cbrainIds.map(pipeline => (
              <li>
                <div className="form-check dropdown-item">
                  <input className="form-check-input" type="radio" name={"datasets" + element.id} id={pipeline.id} value={pipeline.url} onChange={updateSelect} />
                  <label className="form-check-label" htmlFor={pipeline.id}>{pipeline.title}</label>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div> :
          <div className="col">
            <span key={key} data-toggle="tooltip" title="Unavailable" style={{ maxWidth: "140px" }}>
              <a className="btn disabled" href={item.uri} disabled>
                <img className="img-fluid" alt="Online platform" src={item.img} />
              </a>
            </span>
            <button type="button" className="btn btn-outline-secondary dropdown-toggle m-1" disabled>Dataset:</button>
          </div>
  );

  return (
    <div className="card flex-row" style={{ minHeight: '220px' }} data-type="pipeline">
      <div className="col-sm-12 col-md-2 d-flex flex-column justify-content-between align-items-center p-4">
        <a href={element.url}>
          <img
            alt="dataset format"
            className="img-fluid"
            style={{ maxWidth: '140px' }}
            src={
              element.url === undefined
                ? "static/img/cogs-solid-grey.png"
                : "static/img/cogs-solid-green.png"
            }
          />
        </a>
        <div className="d-flex">
          <ViewsIcon type="pipeline" id={element.id} />
          {element.downloads ?
            <DownloadsIcon type="pipeline" id={element.id} /> : null}
        </div>
      </div>
      <div className="card-body d-md-flex flex-wrap">
        <a style={{ color: "inherit" }} href={`pipeline?id=${element.id}`}>
          <h5 className="card-title text-card-title col-12 pl-2 pl-md-0">
            {element.title}
          </h5>
        </a>
        <div className="d-flex col-md-12">
          <div className="card-description d-flex py-1 w-100">
            <div className="col-3">
              <strong>Tags: </strong>
            </div>
            <div className="col-9">{element.tags && element.tags.domain ?
              Array.isArray(element.tags.domain) ?
                element.tags.domain.map(tag => <span key={"tag" + tag} className="mr-1"><a href={"/pipelines?tags=" + tag} className="badge badge-primary">{tag}</a></span>)
                : <span><a href={"/pipelines?tags=" + element.tags.domain} className="badge badge-primary">{element.tags.domain}</a></span>
              : null}
            </div>
          </div>
        </div>
        <div className="d-flex col-md-12">
          <div className="card-description d-flex py-1 w-100">
            <div className="col-3">
              <strong>Description: </strong>
            </div>
            <div className="col-9">{element.description}
            </div>
          </div>
        </div>
        <div className="d-flex col-md-12">
          <div className="card-description text-capitalize d-flex py-1 w-100">
            <div className="col-3">
              <strong>Pipeline ID: </strong>
            </div>
            <div className="col-9">
              <a target="_blank" rel="noopener noreferrer" href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}>{element.id}</a>
            </div>
          </div>
        </div>
      </div>
      <div className="col-sm-12 col-md-3 d-flex align-items-center justify-content-end">
        <div className="d-flex justify-content-end align-items-center">
          {platforms}
          
        </div>
      </div>
    </div>
  );
};

PipelineElement.propTypes = {
  id: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string,
  downloads: PropTypes.number,
  descriptorurl: PropTypes.string,
  platforms: PropTypes.arrayOf(PropTypes.object),
  name: PropTypes.string,
  commandline: PropTypes.string,
  author: PropTypes.string,
  inputs: PropTypes.arrayOf(PropTypes.object),
  outputfiles: PropTypes.arrayOf(PropTypes.object),
  toolversion: PropTypes.string,
  schemaversion: PropTypes.string,
  containerimage: PropTypes.object,
  tags: PropTypes.object,
  url: PropTypes.string,
  img: PropTypes.string,
  imagePath: PropTypes.string,
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
  activeCbrainId: PropTypes.string,
  updateActiveCbrainId: PropTypes.func,
};

//PipelineElement.defaultProps = {
//  imagePath: ""
//};

export default PipelineElement;
