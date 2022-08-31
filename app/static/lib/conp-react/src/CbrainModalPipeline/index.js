import React, { useEffect } from "react";
import * as ReactDOM from "react-dom";
import PropTypes from "prop-types";
const CbrainModalPipeline = (props) => {
  const { platforms, title, cbrainIds } = props;
  const finish = (event) => {
    $("#cbrainModal").modal("hide");
  };
  const baseUrl = platforms[0].uri;
  const getDatasetId = (datasetUrl) =>
    `switch_group_id=${datasetUrl.split("%3Fid%3D")[1]}`;
  useEffect(() => {
    $("#cbrainModal").modal("handleUpdate");

  });
  return ReactDOM.createPortal(
    <div>
      <p>
        You're about to launch <strong>{title}</strong> on CBRAIN. Please select
        a dataset to process with this pipeline (or "None" to load only the
        pipeline).
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
        {cbrainIds.map((dataset) => (
          <a
            href={`${baseUrl}%26${getDatasetId(dataset.url)}`}
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
  title: PropTypes.string,
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
};

export default CbrainModalPipeline;
