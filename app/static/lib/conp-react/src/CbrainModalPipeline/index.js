import React, { useEffect } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalPipeline = (props) => {
  const { authorized, imagePath, ...element } = props;
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };
  const baseUrl = element.platforms[0].uri;
  const getDatasetId = (datasetUrl) =>
    `switch_group_id=${datasetUrl.split("?id=")[1]}`;
  useEffect(() => {
    $("#cbrainModal").modal("handleUpdate");
    return;
  });
  return ReactDOM.createPortal(
    <div>
      <p>
        You're about to load the pipeline <strong>{element.title}</strong> on
        CBRAIN. Please select a dataset to process with this pipeline (or "None"
        to load only the pipeline).
      </p>
      <p>Note that not all pipelines are compatible with all datasets.</p>
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
      <div className="list-group">
        <a
          href={baseUrl}
          className="list-group-item list-group-item-action"
          target="_blank"
          rel="noreferrer"
          key="nonechoice"
          onClick={finish}
        >
          None
        </a>
        {props.cbrainIds.map((dataset) => (
          <a
            href={`${baseUrl}&${getDatasetId(dataset.url)}`}
            className="list-group-item list-group-item-action"
            target="_blank"
            rel="noreferrer"
            key={dataset.title}
            onClick={finish}
          >
            {dataset.title}
          </a>
        ))}
      </div>
    </div>,
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
