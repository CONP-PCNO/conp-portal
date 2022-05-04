import React, { useEffect } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalDataset = (props) => {
  const { authorized, imagePath, ...element } = props;
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };
  const datasetCbrainId = props.cbrain_id.split("?id=")[1];
  const baseUrl = `https://portal.cbrain.mcgill.ca/userfiles?switch_group_id=${datasetCbrainId}`;
  const getPipelineId = (pipelineUrl) => pipelineUrl.split("/userfiles?")[1];

  useEffect(() => {
    $("#cbrainModal").modal("handleUpdate");
    return;
  });

  return ReactDOM.createPortal(
    <div>
      <p>
        You're about to load the dataset <strong>{element.title}</strong> on
        CBRAIN. Please select a pipeline to process this dataset (or "None" to
        load only the dataset).
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
        {props.cbrainIds.map((pipeline) => (
          <a
            href={`${baseUrl}&${getPipelineId(pipeline.url)}`}
            className="list-group-item list-group-item-action"
            target="_blank"
            rel="noreferrer"
            key={pipeline.title}
            onClick={finish}
          >
            {pipeline.title}
          </a>
        ))}
      </div>
    </div>,
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
