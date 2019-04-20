import React from "react";
import PropTypes from "prop-types";

import AppContext from "../AppContext";

const DatasetElement = props => {
  const { authorized, onRunWithCBRAIN, onDownloadMetadata, ...element } = props;

  const context = React.useContext(AppContext);
  const imagePath = (context && context.imagePath) || props.imagePath;

  const runOnCbrainEnabled = `${imagePath}/run_on_cbrain_green.png`;
  const runOnCbrainDisabled = `${imagePath}/run_on_cbrain_gray.png`;
  const downloadEnabled = `${imagePath}/download_green.png`;
  const downloadDisabled = `${imagePath}/download_gray.png`;

  return (
    <div className="search-dataset">
      <div className="dataset-social">
        <img
          alt="dataset format"
          className="dataset-social-img"
          src={element.thumbnailURL}
        />
        <div className="dataset-social-icons">
          <div className="dataset-social-icon">
            <i className="fa fa-download social-fa" />
            <div>{element.downloads}</div>
          </div>
          <div className="dataset-social-icon">
            <i className="fa fa-eye social-fa" />
            <div>{element.views}</div>
          </div>
          <div className="dataset-social-icon">
            <i className="fa fa-heart social-fa" />
            <div>{element.likes}</div>
          </div>
        </div>
      </div>
      <div className="dataset-details">
        <div className="dataset-details-stats">
          <div className="dataset-title">
            <div><a style={{ color: "inherit" }} href={`dataset?id=${element.id}`}>{element.title}</a></div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Date Added</div>
            <div className="dataset-stat-num">{element.dateAdded}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Date Updated</div>
            <div className="dataset-stat-num">{element.dateUpdated}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Size</div>
            <div className="dataset-stat-num">{element.size}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Files</div>
            <div className="dataset-stat-num">{element.files}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Subjects</div>
            <div className="dataset-stat-num">{element.subjects}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Format</div>
            <div className="dataset-stat-num">{element.format}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Modalities</div>
            <div className="dataset-stat-num">{element.modalities}</div>
          </div>
          <div className="dataset-stat">
            <div className="dataset-stat-text">Sources</div>
            <div className="dataset-stat-num">{element.sources}</div>
          </div>
        </div>
        <div className="dataset-options">
          <div className="dataset-option">
            <img
              alt="Run On Cbrain"
              className="run-on-cbrain-button option-icon"
              src={
                element.isPublic || authorized
                  ? runOnCbrainEnabled
                  : runOnCbrainDisabled
              }
              onClick={event => {
                event.preventDefault();
                if (!(element.isPublic || authorized)) {
                  return;
                }
                onRunWithCBRAIN instanceof Function &&
                  onRunWithCBRAIN(props, event);
              }}
            />
          </div>
          <div className="dataset-option">
            <img
              alt="Download Metadata"
              className="download-button  option-icon"
              src={
                element.isPublic || authorized
                  ? downloadEnabled
                  : downloadDisabled
              }
              onClick={event => {
                event.preventDefault();
                if (!(element.isPublic || authorized)) {
                  return ;
                }
                onDownloadMetadata instanceof Function &&
                  onDownloadMetadata(props, event);
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

DatasetElement.propTypes = {
  authorized: PropTypes.bool,
  onRunWithCBRAIN: PropTypes.func,
  onDownloadMetadata: PropTypes.func,
  // element proptypes
  id: PropTypes.string,
  title: PropTypes.string,
  isPublic: PropTypes.bool,
  thumbnailURL: PropTypes.string,
  downloads: PropTypes.number,
  views: PropTypes.number,
  likes: PropTypes.number,
  dateAdded: PropTypes.string,
  dateUpdated: PropTypes.string,
  size: PropTypes.string,
  files: PropTypes.number,
  subjects: PropTypes.number,
  format: PropTypes.string,
  modalities: PropTypes.string,
  sources: PropTypes.number
};

export default DatasetElement;
