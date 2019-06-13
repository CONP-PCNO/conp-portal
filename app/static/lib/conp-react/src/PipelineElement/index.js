import React from "react";
import PropTypes from "prop-types";

const PipelineElement = props => {
  const { authorized, ...element } = props;

  return (
    <div className="search-pipeline">
      <div className="pipeline-id">
        <a style={{ color: "inherit" }} href={element.url}>
          {element.id}
        </a>
      </div>
      <div className="pipeline-title">
        {element.title}
      </div>
      <div className="pipeline-description">
        {element.description}
      </div>
      <div className="pipeline-downloads">
        {element.downloads}
      </div>
    </div>
  );
};

PipelineElement.propTypes = {
  id: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string,
  downloads: PropTypes.number,
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
