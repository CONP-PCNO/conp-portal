import React from "react";
import PropTypes from "prop-types";

const PipelineElement = props => {
  const { authorized, ...element } = props;
  const platforms = element.platforms.map((item,key) =>
    <a key={key} className="card-button mx-2" href={item.uri}>
      <img alt="Online platform" src={item.img} />
    </a>
  );

  return (
    <div className="card row flex-row" data-type="pipeline">
      <div className="col-xs-12 col-sm-6 col-md-3 col-lg-2 card-img card-social">
        <a href={element.url}>
          <img
            alt="dataset format"
            className="card-img-top card-social-img"
            src={
              element.url == undefined
                ? "static/img/cogs-solid-grey.png"
                : "static/img/cogs-solid-green.png"
            }
          />
        </a>
        <div className="card-social-icons">
          {element.downloads ?
          <div className="card-social-icon">
            <i className="fa fa-download my-2" />
            <div>{element.downloads}</div>
          </div> : null }
        </div>
      </div>
      <div className="card-body d-md-flex flex-wrap">
        <a
          style={{
            color: "inherit",
            pointerEvents: element.descriptorurl == undefined ? "none" : "all"
          }}
          href={element.descriptorurl}
        >
          <h5 className="card-title text-card-title col-12 pl-2 pl-md-0">
            {element.title}
          </h5>
        </a>
        <div className="card-subtitle col-12 pl-2 pl-md-0">
          <p className="card-text text-capitalize pr-1">
            <strong>Pipeline Id:</strong>
          </p>
          <a href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}>
            <p className="card-text text-muted text-link">{element.id}</p>
          </a>
        </div>
        <div className="d-flex col-md-12 px-2">
          <div className="card-description">{element.description}</div>
        </div>
      </div>
      <div className="col-12 col-md-auto d-flex align-items-center justify-content-center my-2 card-buttons">
        <div className="d-flex justify-content-end align-items-center flex-wrap">
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
