import React from "react";
import PropTypes from "prop-types";

const PipelineElement = props => {
  const { authorized, ...element } = props;
  const platforms = element.platforms.map((item, key) =>
    item.uri ?
      <span key={key} data-toggle="tooltip" title="Run Pipeline" style={{ maxWidth: "140px" }}>
        <a className="btn" href={item.uri}>
          <img className="img-fluid" alt="Online platform" src={item.img} />
        </a>
      </span> :
      <span key={key} data-toggle="tooltip" title="Unavailable" style={{ maxWidth: "140px" }}>
        <a className="btn disabled" href={item.uri} disabled>
          <img className="img-fluid" alt="Online platform" src={item.img} />
        </a>
      </span>
  );

  return (
    <div className="card flex-row" data-type="pipeline">
      <div className="col-sm-12 col-md-2 d-flex flex-column justify-content-between align-items-center p-4">
        <a href={element.url}>
          <img
            alt="dataset format"
            className="img-fluid"
            src={
              element.url == undefined
                ? "static/img/cogs-solid-grey.png"
                : "static/img/cogs-solid-green.png"
            }
          />
        </a>
        <div className="d-flex">
          {element.downloads ?
            <div className="d-flex flex-column align-items-center">
              <i className="fa fa-download my-2" />
              <div>{element.downloads}</div>
            </div> : null}
        </div>
      </div>
      <div className="card-body d-md-flex flex-wrap">
        <a style={{ color: "inherit" }} href={`pipeline?id=${element.id}`}>
          <h5 className="card-title text-card-title col-12 pl-2 pl-md-0">
            {element.title}
          </h5>
        </a>
        <div className="d-flex col-md-12">
          <p className="card-text text-capitalize pr-1">
            <strong>Pipeline Id: </strong>
            <a target="_blank" rel="noopener noreferrer" href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}>{element.id}</a>
          </p>
        </div>
        <div className="d-flex col-md-12">
          <div className="card-description">{element.description}</div>
        </div>
      </div>
      <div className="col-sm-12 col-md-4 d-flex align-items-center justify-content-end">
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
  imagePath: PropTypes.string
};

//PipelineElement.defaultProps = {
//  imagePath: ""
//};

export default PipelineElement;
