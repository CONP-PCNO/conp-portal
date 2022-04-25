import React, { useState } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalDataset = (props) => {
  const { authorized, imagePath, ...element } = props;
  const [phaseState, setPhaseState] = useState(0);
  const updateSelect = (event) => {
    props.updateActiveCbrainId(props.id, event.target.value);
    setPhaseState(1);
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
              You're about to load the dataset <strong>{element.title}</strong>{" "}
              on CBRAIN. Please select a pipeline to process this dataset (or
              "None" to load only the dataset).
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
                aria-label="pipeline"
              >
                Pipeline:
              </button>
              <ul
                className="dropdown-menu"
                aria-labelledby={"dropdown" + element.id}
              >
                <li>
                  <div className="form-check dropdown-item">
                    <input
                      className="form-check-input"
                      type="radio"
                      name={"pipelines" + element.id.replaceAll("/", "")}
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
                        name={"pipelines" + element.id.replaceAll("/", "")}
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
              <strong>{element.title}</strong>, then return to this page to
              prepare the pipeline.
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
              before loading the dataset.
            </p>
            <a
              href={props.cbrain_id}
              target="_blank"
              rel="noreferrer"
              className={
                "btn " + (phaseState === 1 ? "btn-primary" : "btn-secondary")
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
              <strong>
                {element.activeCbrainId === ""
                  ? null
                  : element.cbrainIds.filter(
                      (pipeline) => pipeline.url === element.activeCbrainId
                    )[0].title}
              </strong>{" "}
              for processing the dataset <strong>{element.title}</strong>.
            </p>
            <a
              href={props.activeCbrainId}
              target="_blank"
              rel="noreferrer"
              className={
                "btn " +
                (phaseState === 2 ? "btn-primary" : "btn-secondary") +
                (props.activeCbrainId === "" ? " disabled" : "")
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

CbrainModalDataset.propTypes = {
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

CbrainModalDataset.defaultProps = {
  imagePath: "",
  downloadPath: "",
};

export default CbrainModalDataset;
