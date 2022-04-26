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
      <div className="container-fluid">
        <div className="row align-items-center">
          <div className={"col-lg-4 " + (phaseState === 0 ? "" : "text-muted")}>
            <p>
              You're about to load the pipeline <strong>{element.title}</strong>{" "}
              on CBRAIN. Please select a dataset to process with this pipeline
              (or "None" to load only the pipeline).
            </p>
            <p>Note that not all pipelines are compatible with all datasets.</p>
            <div className="dropdown">
              <button
                type="button"
                className={
                  "dropdown-toggle btn " +
                  (phaseState === 0 ? "btn-primary" : "btn-secondary")
                }
                data-toggle="dropdown"
                data-display="static"
                aria-expanded="false"
                aria-label="dataset"
              >
                Dataset:
              </button>
              <ul
                className="dropdown-menu"
                aria-labelledby={"dropdown" + element.id}
              >
                <li>
                  <div className="form-check dropdown-item">
                    <input
                      type="radio"
                      className="form-check-input"
                      name={"datasets" + element.id}
                      id="nonechoice"
                      key="nonechoice"
                      onChange={updateSelect}
                      value=""
                    />
                    <label className="form-check-label" htmlFor="nonechoice">
                      None
                    </label>
                  </div>
                </li>
                {props.cbrainIds.map((pipeline) => (
                  <li>
                    <div className="form-check dropdown-item">
                      <input
                        type="radio"
                        className="form-check-input"
                        name={"datasets" + element.id}
                        id={pipeline.title}
                        key={pipeline.title}
                        value={pipeline.url}
                        onChange={updateSelect}
                      />
                      <label
                        className="form-check-label"
                        htmlFor={pipeline.title}
                      >
                        {pipeline.title}
                      </label>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className={"col-lg-4 " + (phaseState === 1 ? "" : "text-muted")}>
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
            <a
              href={element.activeCbrainId}
              target="_blank"
              rel="noreferrer"
              className={
                "btn " +
                (phaseState === 1 ? "btn-primary" : "btn-secondary") +
                (element.activeCbrainId === "" ? " disabled" : "")
              }
              onClick={
                element.activeCbrainId === "" ? finish : showPipelineButton
              }
            >
              Load dataset
            </a>
          </div>
          <div className={"col-lg-4 " + (phaseState === 2 ? "" : "text-muted")}>
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
              className={
                "btn " + (phaseState === 2 ? "btn-primary" : "btn-secondary")
              }
              onClick={finish}
            >
              Prepare pipeline
            </a>
          </div>
        </div>
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
