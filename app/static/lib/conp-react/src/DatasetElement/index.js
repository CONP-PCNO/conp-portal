import React from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserLock } from '@fortawesome/free-solid-svg-icons'
import { faUserAlt } from '@fortawesome/free-solid-svg-icons'
import { faFileCode } from '@fortawesome/free-regular-svg-icons'

const DatasetElement = props => {
  const { authorized, imagePath, ...element } = props;

  const downloadEnabled = `${imagePath}/download_green.png`;
  const downloadDisabled = `${imagePath}/download_gray.png`;

  const statusCONP = `${imagePath}/canada.svg`;

  let authIcons = [];
  switch (element.authorizations) {
    case 'restricted':
      authIcons.push(<span><FontAwesomeIcon icon={faUserAlt} color="dimgray" size="lg" /> - CONP account required</span>);
      break;
    case 'private':
      authIcons.push(<span><FontAwesomeIcon icon={faUserLock} color="dimgray" size="lg" /> - Third-party account required</span>);
      break;
    default:
      break;
  }

  var ciBadges = [];
  var color;
  switch (element.status) {
    case "Working":
      color = "success";
      break;
    case "Warning":
      color = "important";
      break;
    default:
      color = "critical";
      break;
  }
  let url =
    "https://img.shields.io/badge/circleci-" +
    element.status +
    "-" +
    color +
    "?style=flat-square&logo=circleci" +
    "&link=" +
    element.latest_build_url;
  ciBadges.push(<img key={"badge_" + color} src={url} alt="CircleCI status" />);

  return (
    <div className="card d-flex flex-row" style={{minHeight: '220px'}} data-type="dataset">
      <div className="card-header d-flex flex-column justify-content-between">
        <div className="d-flex justify-content-center">
          {element.conpStatus !== 'external' ? (<img height="32" width="32" src={statusCONP} />) : <div style={{ width: 32 }} />}
        </div>
      </div>
      <div className="col-2 d-flex align-items-center">
        <img
          alt="dataset format"
          className="img-fluid"
          style={{maxWidth: '160px'}}
          src={element.logoFilepath.startsWith('http') ? element.logoFilepath : element.thumbnailURL}
        />
      </div>
      <div className="col-7 card-body d-flex flex-wrap">
        <h5 className="card-title text-card-title col-12 pl-2 pl-md-0">
          <a style={{ color: "inherit" }} href={`dataset?id=${element.id}`}>
            {element.title}
          </a>
          <a style={{ color: "inherit", 'margin-left' : "10px" }}
             href="https://app.circleci.com/pipelines/github/CONP-PCNO/conp-dataset?branch=master"
          >
            {ciBadges.map(badge => badge)}
          </a>
        </h5>
        <ul className="d-flex">
          {element.principalInvestigators ?
            <li className="card-list-item">
              <p className="card-text pr-1">
                <strong>Principal Investigator: </strong>{element.principalInvestigators.toString()}
              </p>
            </li> : null}
          {element.sources ?
            <li className="card-list-item">
              <p className="card-text pr-1">
                <strong>Sources: </strong>
                <a target="_blank" rel="noopener noreferrer" href={element.sources}>{element.sources}</a>
              </p>
            </li> : null}
          {element.files ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Files: </strong>{element.files}
              </p>
            </li> : null}
          {element.size ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Size: </strong>{element.size}
              </p>
            </li> : null}
          {element.subjects ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Subjects: </strong>{element.subjects}
              </p>
            </li> : null}
          {element.format ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Format: </strong>{element.format.toString()}
              </p>
            </li> : null}
          {element.modalities ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Modalities: </strong>{element.modalities}
              </p>
            </li> : null}
          {element.dateAdded ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Date Added: </strong>{element.dateAdded
                }</p>
            </li> : null}
          {element.dateUpdated ?
            <li className="card-list-item">
              <p className="card-text text-capitalize pr-1">
                <strong>Date Updated: </strong>{element.dateUpdated}
              </p>
            </li> : null}
        </ul>
        <div className="d-flex justify-content-center">
          <div className="d-flex">
            {authIcons.map((icon, index) => <div key={"authIcon_" + index} className="p-1">{icon}</div>)}
          </div>
        </div>
      </div>
      <div className="col-2 d-flex flex-column justify-content-center align-items-end">
        {element.showDownload ? <a
          className="card-button"
          style={{
            pointerEvents: element.isPrivate && !authorized ? "none" : "all",
            maxWidth: "160px"
          }}
          href={`download_metadata?dataset=${element.id}`}
          download
        >
          {element.isPrivate && !authorized && (
            <div className="card-button-tooltip">
              Please register for access.
            </div>
          )}
          <div className="d-flex flex-column align-items-center">
            <FontAwesomeIcon icon={faFileCode} color="black" size="6x" />
            <button className="btn btn-link text-nowrap">Download Metadata</button>
          </div>
        </a> : null}
      </div>
    </div>
  );
};

DatasetElement.propTypes = {
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

DatasetElement.defaultProps = {
  imagePath: "",
  downloadPath: ""
};

export default DatasetElement;
