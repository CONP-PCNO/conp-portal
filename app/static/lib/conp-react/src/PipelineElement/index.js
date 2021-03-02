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
    <div className="card container-fluid" data-type="pipeline">
      <div className="row">
        <div className="col col-lg-2 d-flex flex-column p-2">
          <div className="flex-grow-2 d-flex flex-column h-100 justify-content-center align-items-center">
            <a href={element.url}>
              <img
                alt="dataset format"
                className="img-fluid w-100"
                style={{ maxWidth: '180px' }}
                src={
                  element.url === undefined
                    ? "static/img/cogs-solid-grey.png"
                    : "static/img/cogs-solid-green.png"
                }
              />
            </a>
          </div>
          <div className="flex-grow-1 d-flex flex-row align-items-end">
            {element.downloads ?
              <div className="d-flex flex-column align-items-center">
                <i className="fa fa-download my-2" />
                <div>{element.downloads}</div>
              </div> : null}
          </div>
        </div>
        <div className="col col-lg-8 card-body d-flex">
          <div className="d-flex flex-column">
            <h5 className="card-title text-card-title">
              <a className="text-reset" href={`pipeline?id=${element.id}`}>
                {element.title}
              </a>
            </h5>
            <div className="py-2">
              <ul className="d-flex flex-column align-items-start">
                {element.tags && element.tags.domain ?
                  <li className="card-list-item">
                    <strong>Tags: </strong>
                    {Array.isArray(element.tags.domain) ?
                      element.tags.domain.map(tag => <span key={"tag" + tag} className="mr-1"><a href={"/pipelines?tags=" + tag} className="badge badge-primary">{tag}</a></span>)
                      : <span><a href={"/pipelines?tags=" + element.tags.domain} className="badge badge-primary">{element.tags.domain}</a></span>}
                  </li> : null}
                {element.description ?
                  <li className="card-list-item">
                    <strong>Description: </strong>{element.description}
                  </li> : null}
                {element.id ?
                  <li className="card-list-item">
                    <strong>Pipeline ID: </strong><a target="_blank" rel="noopener noreferrer" href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}>{element.id}</a>
                  </li> : null}
              </ul>

            </div>
          </div>
        </div>
        <div className="col col-lg-2 d-flex flex-column justify-content-center align-items-center p-2">
          {platforms}
        </div>
      </div >
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
