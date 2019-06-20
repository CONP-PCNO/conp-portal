import React from "react";
import PropTypes from "prop-types";

const PipelineElement = props => {
  const { authorized, ...element } = props;

  const imagePath = element.imagePath;
  const runOnCbrainEnabled = `${imagePath}/run_on_cbrain_green.png`;
  const runOnCbrainDisabled = `${imagePath}/run_on_cbrain_gray.png`;
  const downloadEnabled = `${imagePath}/download_green.png`;
  const downloadDisabled = `${imagePath}/download_gray.png`;

  return (
    <div className="search-dataset">
      <div className="dataset-social">
        <a href={element.url}>
          <img
            alt="dataset format"
            className="dataset-social-img"
            src="static/img/cogs-solid.svg"
          />
        </a>
        <div className="dataset-social-icons">
          <div className="dataset-social-icon">
            <i className="fa fa-download social-fa" />
            <div>{element.downloads}</div>
          </div>
        </div>
      </div>
      <div className="dataset-details">
        <div className="dataset-details-stats">
          <div className="pipeline-title">
            <div>
              <a style={{ color: "inherit", pointerEvents: element.descriptorurl == undefined ? "none" : "all" }}
              href={element.descriptorurl}>
                {element.title}
              </a>
            </div>
          </div>
          <div className="pipeline-id">
            <a style={{ color: "black" }} href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}>
              {element.id}
            </a>
          </div>
          <div className="pipeline-description">
            {element.description}
          </div>
        </div>
        <div className="dataset-options">
          <div className="dataset-option">
            <a href={element.onlineplatformurls}>
              <img
                alt="Online platform"
                className="run-on-cbrain-button option-icon"
                src={"static/img/globe-solid.svg"}
              />
            </a>
          </div>
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
  onlineplatformurls: PropTypes.string,
  name: PropTypes.string,
  commandline: PropTypes.string,
  author: PropTypes.string,
  inputs: PropTypes.arrayOf(PropTypes.object),
  outputfiles: PropTypes.arrayOf(PropTypes.object),
  toolversion: PropTypes.string,
  schemaversion: PropTypes.string,
  containerimage: PropTypes.object,
  tags: PropTypes.object,
  url: PropTypes.string
};

//PipelineElement.defaultProps = {
//  imagePath: "",
//  downloadPath: ""
//};

export default PipelineElement;
