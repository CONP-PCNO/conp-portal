import React from "react";
import PropTypes from "prop-types";

const PipelineExecutionRecordElement = props => {
  const { authorized, ...element } = props;

  return (
    <div className="card flex-row" style={{ minHeight: '50px' }} data-type="pipeline">
      <div className="d-flex col-md-12">
        <div className="d-flex py-1 w-100" style={{ fontSize: 20 }}>
          <div className="col-5">
            <span >
              <a target="_blank" href={element.pipelineUrl} title="Browse Pipeline">{element.pipelineName}</a>
            </span>
          </div>
          <div className="col-5">
            <span >
              <a target="_blank" href={element.datasetUrl} title="Browse Dataset">{element.datasetName}</a>
            </span>
          </div>
          <div className="col-2">
            <span >
              <a target="_blank" href={element.executionRecordUrl} title="Browse Execution Record">{element.executionRecord}</a>
            </span>
          </div>
        </div>
      </div>
    </div>
	  
	  
  );
};

PipelineExecutionRecordElement.propTypes = {
  pipelineName : PropTypes.string,
  pipelineUrl : PropTypes.string,
  datasetName : PropTypes.string,
  datasetUrl : PropTypes.string,
  executionRecord : PropTypes.string,
  executionRecordUrl : PropTypes.string,
};


export default PipelineExecutionRecordElement;





