import React from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserLock } from '@fortawesome/free-solid-svg-icons'
import { faUserAlt } from '@fortawesome/free-solid-svg-icons'

const DatasetElement = props => {
  const { authorized, imagePath, ...element } = props;

  const runOnCbrainEnabled = `${imagePath}/run_on_cbrain_green.png`;
  const runOnCbrainDisabled = `${imagePath}/run_on_cbrain_gray.png`;
  const downloadEnabled = `${imagePath}/download_green.png`;
  const downloadDisabled = `${imagePath}/download_gray.png`;

  const statusCONP = `${imagePath}/canada.svg`;
  let authIcons = [];

  switch (element.authorizations) {
    case 'restricted':
      authIcons.push(<FontAwesomeIcon icon={faUserAlt} color="black" size="lg"/>);
      break;
    case 'private':
      authIcons.push(<FontAwesomeIcon icon={faUserLock} color="black" size="lg"/>);
      break;
    default:
      break;
  }

  return (
    <div className="card row flex-row" data-type="dataset">
      <div className="card-header d-flex flex-column justify-content-between">
        <div className="d-flex justify-content-center">
          {element.conpStatus !== 'external' ? (<img height="32" width="32" src={statusCONP}/>) : <div style={{width: 32}}/>}
        </div>
        <div className="d-flex justify-content-center">
          <div className="d-flex">
            {authIcons.map(icon => <div className="p-1">{icon}</div>)}
          </div>
        </div>
      </div>
      <div className="col-xs-12 col-sm-6 col-md-3 col-lg-2 card-img card-social">
        <img
          alt="dataset format"
          className="card-img-top card-social-img"
          src={element.thumbnailURL}
        />
      </div>
      <div className="card-body d-md-flex flex-wrap">
        <a style={{ color: "inherit" }} href={`dataset?id=${element.id}`}>
          <h5 className="card-title text-card-title col-12 pl-2 pl-md-0">
            {element.title}
          </h5>
        </a>
        <ul className="d-flex col-md-12 px-1 px-md-0 card-list">
          {element.files ?
          <li className="card-list-item">
            <p className="card-text text-capitalize pr-1">
              <strong>Files: </strong>
            </p>
            <p className="card-text text-muted">{element.files}</p>
          </li> : null }
          {element.size ?
          <li className="card-list-item">
            <p className="card-text text-capitalize pr-1">
              <strong>Size: </strong>
            </p>
            <p className="card-text text-muted">{element.size}</p>
          </li> : null }
          {element.subjects ?
          <li className="card-list-item">
            <p className="card-text text-capitalize pr-1">
              <strong>Subjects: </strong>
            </p>
            <p className="card-text text-muted">{element.subjects}</p>
          </li> : null }
          {element.sources ?
          <li className="card-list-item">
            <p className="card-text text-capitalize pr-1">
              <strong>Sources: </strong>
            </p>
            <a className="card-text btn-link" href={element.sources}>{element.sources}</a>
          </li> : null }
          {element.format ? 
          <li className="card-list-item">
            <p className="card-text text-capitalize pr-1">
              <strong>Format: </strong>
            </p>
            <p className="card-text text-muted">{element.format.toString()}</p>
          </li> : null }
          {element.modalities ? 
          <li className="d-none d-md-flex">
            <p className="card-text text-capitalize pr-1">
              <strong>Modalities: </strong>
            </p>
            <p className="card-text text-muted">{element.modalities}</p>
          </li> : null }
          {element.updated ?
          <li className="d-none d-md-flex">
            <p className="card-text text-capitalize pr-1">
              <strong>Date Updated: </strong>
            </p>
            <p className="card-text text-muted">{element.dateUpdated}</p>
          </li> : null}
        </ul>
      </div>
      <div className="col-12 col-md-auto d-flex my-2 card-buttons">
        <button className="btn btn-outline-secondary d-md-none">
          Go to Dataset
        </button>
        <div className="d-flex justify-content-end align-items-center flex-wrap mb-3 mb-md-0">

          <a
            className="card-button mx-2"
            style={{
              pointerEvents: element.isPrivate && !authorized ? "none" : "all"
            }}
            href={`download_metadata?dataset=${element.id}`}
            download
          >
            {element.isPrivate && !authorized && (
              <div className="card-button-tooltip">
                Please register for access.
              </div>
            )}

            <img
              alt="Download Metadata"
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
