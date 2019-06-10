import React from "react";
import PropTypes from "prop-types";

const PipelineElement = props => {
  const { authorized, ...element } = props;

  const imagePath = element.imagePath;
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
            <div>
              <a style={{ color: "inherit" }} href={`dataset?id=${element.id}`}>
                {element.title}
              </a>
            </div>
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
            <a
              href={"#"}
              style={{
                pointerEvents: element.isPrivate && !authorized ? "none" : "all"
              }}
            >
            >
              <img
                alt="Run On Cbrain"
                className="run-on-cbrain-button option-icon"
                src={
                  element.isPrivate && !authorized
                    ? runOnCbrainDisabled
                    : runOnCbrainEnabled
                }
              />
            </a>
          </div>
          <div className="dataset-option" style={{ position: "relative" }}>
            <a
              style={{
                pointerEvents: element.isPrivate && !authorized ? "none" : "all"
              }}
              href={`download_metadata?dataset=${element.downloadPath}`}
              download
            >
              {element.isPrivate && !authorized && (
                <div
                  style={{
                    backgroundColor: "white",
                    padding: "5px",
                    border: "solid black",
                    color: "black",
                    borderWidth: "1px",
                    left: "-30px",
                    textAlign: "center",
                    position: "absolute"
                  }}
                >
                  Please register for access.
                </div>
              )}
              <img
                alt="Download Metadata"
                className="download-button  option-icon"
                src={
                  element.isPrivate && !authorized
                    ? downloadDisabled
                    : downloadEnabled
                }
              />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

PipelineElement.propTypes = {
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
  format: PropTypes.string,
  modalities: PropTypes.string,
  sources: PropTypes.number
};

PipelineElement.defaultProps = {
  imagePath: "",
  downloadPath: ""
};

export default PipelineElement;
