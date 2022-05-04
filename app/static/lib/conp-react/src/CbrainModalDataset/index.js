import React, { useEffect } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalDataset = (props) => {
  const { cbrain_id, cbrainIds, title } = props;
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };
  const datasetCbrainId = cbrain_id.split("?id=")[1];
  const baseUrl = `https://portal.cbrain.mcgill.ca/userfiles?switch_group_id=${datasetCbrainId}`;
  const getPipelineId = (pipelineUrl) => pipelineUrl.split("/userfiles?")[1];

  useEffect(() => {
    $("#cbrainModal").modal("handleUpdate");
    return;
  });

  return ReactDOM.createPortal(
    <div>
      <p>
        You're about to load the dataset <strong>{title}</strong> on
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
        {cbrainIds.map((pipeline) => (
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
  title: PropTypes.string,
  cbrain_id: PropTypes.string,
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
};

CbrainModalDataset.defaultProps = {
  imagePath: "",
  downloadPath: "",
};

export default CbrainModalDataset;
