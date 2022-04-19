import React, { useState } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalPipeline = (props) => {
  const { authorized, imagePath, ...element } = props;
  const [phaseState, setPhaseState] = useState(0);
  const updateSelect = (event) => {
    props.updateActiveCbrainId(props.id, event.target.value);
    if (event.target.value === "") {
      setPhaseState(2);
    } else {
      setPhaseState(1);
    }
  };
  const showPipelineButton = (event) => {
    setPhaseState(2);
  };
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };

  return ReactDOM.createPortal(
    <>
      <div className={phaseState === 0 ? null : "d-none"}>
        <p>
          You're about to load the pipeline <strong>{element.title}</strong> on
          CBRAIN. Please select a dataset to process with this pipeline (or
          "None" to load only the pipeline).
        </p>
        <p>
          Please ensure you're{" "}
          <a
            href="https://portal.cbrain.mcgill.ca"
            target="_blank"
            rel="noreferrer"
          >
            logged into CBRAIN
          </a>{" "}
          before loading the pipeline.
        </p>
        <p>Note that not all pipelines are compatible with all datasets.</p>
        <div className="list-group">
          <button
            type="button"
            className="list-group-item list-group-item-action"
            id="nonechoice"
            key="nonechoice"
            onClick={updateSelect}
            value=""
          >
            None
          </button>
          {props.cbrainIds.map((pipeline) => (
            <button
              type="button"
              className="list-group-item list-group-item-action"
              id={pipeline.title}
              key={pipeline.title}
              value={pipeline.url}
              onClick={updateSelect}
            >
              {pipeline.title}
            </button>
          ))}
        </div>
      </div>
      <div className={phaseState === 1 ? null : "d-none"}>
        <p>
          Press the button to load the dataset{" "}
          <strong>
            {element.activeCbrainId === ""
              ? null
              : element.cbrainIds.filter(
                  (dataset) => dataset.url === element.activeCbrainId
                )[0].title}
          </strong>
          , then return to this page to prepare the pipeline.
        </p>
        <a
          href={element.activeCbrainId}
          target="_blank"
          rel="noreferrer"
          className="btn btn-primary"
          onClick={element.activeCbrainId === "" ? finish : showPipelineButton}
        >
          Load dataset
        </a>
      </div>
      <div className={phaseState === 2 ? null : "d-none"}>
        <p>
          Press the button to prepare the pipeline{" "}
          <strong>{element.title}</strong>
          {element.activeCbrainId === "" ? null : (
            <>
              {" "}
              for processing the dataset{" "}
              <strong>
                {
                  element.cbrainIds.filter(
                    (dataset) => dataset.url === element.activeCbrainId
                  )[0].title
                }
              </strong>
            </>
          )}
          .
        </p>
        <a
          href={element.platforms[0].uri}
          target="_blank"
          rel="noreferrer"
          className="btn btn-primary"
          onClick={finish}
        >
          Prepare pipeline
        </a>
      </div>
    </>,
    document.querySelector("#cbrainModalBody")
  );
};

CbrainModalPipeline.propTypes = {
  authorized: PropTypes.bool,
  onRunWithCBRAIN: PropTypes.func,
  // element proptypes
  id: PropTypes.string,
  title: PropTypes.string,
  isPrivate: PropTypes.bool,
  thumbnailURL: PropTypes.string,
  imagePath: PropTypes.string,
  downloadPath: PropTypes.string,
  downloads: PropTypes.number,
  views: PropTypes.number,
  likes: PropTypes.number,
  dateAdded: PropTypes.string,
  dateUpdated: PropTypes.string,
  size: PropTypes.string,
  files: PropTypes.number,
  subjects: PropTypes.number,
  formats: PropTypes.string,
  modalities: PropTypes.string,
  sources: PropTypes.number,
  cbrain_id: PropTypes.string,
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
  activeCbrainId: PropTypes.string,
  updateActiveCbrainId: PropTypes.func,
};

CbrainModalPipeline.defaultProps = {
  imagePath: "",
  downloadPath: "",
};

export default CbrainModalPipeline;
