import React, { useEffect } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalDataset = (props) => {
  const { cbrain_id, cbrainIds, title } = props;
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };
  const datasetCbrainId = cbrain_id.split("%3Fid%3D")[1];
  const baseUrl = `https%3A%2F%2Fportal.cbrain.mcgill.ca%2Fuserfiles%3Fswitch_group_id%3D${datasetCbrainId}`;
  const getPipelineId = (pipelineUrl) => pipelineUrl.split("/userfiles?")[1];

  useEffect(() => {
    $("#cbrainModal").modal("handleUpdate");

  });

  return ReactDOM.createPortal(
    <div>
      <p>
        You're about to load <strong>{title}</strong> on CBRAIN. Please select a
        pipeline to process this dataset (or "None" to load only the dataset).
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
        before loading the dataset.
      </p>
      <div className="list-group">
        <a
          href={cbrain_id}
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
            href={`${pipeline.url}%26switch_group_id%3D${datasetCbrainId}`}
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
