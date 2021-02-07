import React from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserLock } from '@fortawesome/free-solid-svg-icons'
import { faUserAlt } from '@fortawesome/free-solid-svg-icons'
import { faFileCode } from '@fortawesome/free-regular-svg-icons'

const DatasetElement = props => {
  const { authorized, imagePath, ...element } = props;

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

  console.log(element)

  return (
    <div className="card d-flex flex-row" data-type="dataset">
      <div className="d-flex flex-column justify-content-between">
        <div className="flex-grow-2">
          <img
            alt="dataset format"
            className="img-fluid"
            style={{ maxWidth: '160px' }}
            src={element.logoFilepath.startsWith('http') ? element.logoFilepath : element.thumbnailURL}
          />
        </div>
        <div className="d-flex flex-row justify-content-center">
          {element.conpStatus !== 'external' ? (<img height="32" width="32" src={statusCONP} alt="CONP status" />) : <div style={{ width: 32 }} />}
          {element.conpStatus !== 'external' ? (<img height="32" width="32" src={statusCONP} alt="CONP status" />) : <div style={{ width: 32 }} />}
          {element.conpStatus !== 'external' ? (<img height="32" width="32" src={statusCONP} alt="CONP status" />) : <div style={{ width: 32 }} />}
        </div>
      </div>
      <div className="card-body d-flex">
        <div className="d-flex flex-column w-100">
          <h5 className="card-title text-card-title">
            <a style={{ color: "inherit" }} href={`dataset?id=${element.id}`}>
              {element.title}
            </a>
          </h5>
          <div className="py-2">
            <div className="d-flex align-items-start">
              {element.creators ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong>Creators: </strong>{element.creators}
                  </p>
                </div> : null}
              {element.origin?.institution ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong> | </strong>
                    <strong>Institution: </strong>{element.origin.institution}
                  </p>
                </div> : null}
              {element.origin?.consortium ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong> | </strong>
                    <strong>Consortium: </strong>{element.origin.consortium}
                  </p>
                </div> : null}
            </div>
            <div className="d-flex align-items-start">
              {element.dateAdded ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong>Date Added: </strong>{element.dateAdded}
                  </p>
                </div> : null}
              {element.dateUpdated ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong> | </strong>
                    <strong>Date Updated: </strong>{element.dateUpdated}
                  </p>
                </div> : null}
            </div>
            <div className="d-flex align-items-start">
              {element.version ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong>Version: </strong>{element.version}
                  </p>
                </div> : null}
              {element.types ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong> | </strong>
                    <strong>Data Types: </strong>{element.types}
                  </p>
                </div> : null}
              {element.modalities ?
                <div className="card-list-item">
                  <p className="card-text pr-1">
                    <strong> | </strong>
                    <strong>Modalities: </strong>{element.modalities}
                  </p>
                </div> : null}
              {element.licenses ?
                <div className="card-list-item">
                  <p className="card-text text-capitalize pr-1">
                    <strong> | </strong>
                    <strong>License: </strong>{element.licenses}
                  </p>
                </div> : null}
            </div>
            <div className="d-flex align-items-start">
              {element.files ?
                <div className="card-list-item">
                  <p className="card-text text-capitalize pr-1">
                    <strong>Files: </strong>{element.files}
                  </p>
                </div> : null}
              {element.size ?
                <div className="card-list-item">
                  <p className="card-text text-capitalize pr-1">
                    <strong> | </strong>
                    <strong>Size: </strong>{element.size}
                  </p>
                </div> : null}
              {element.subjects ?
                <div className="card-list-item">
                  <p className="card-text text-capitalize pr-1">
                    <strong> | </strong>
                    <strong>Subjects: </strong>{element.subjects}
                  </p>
                </div> : null}
              {element.formats ?
                <div className="card-list-item">
                  <p className="card-text text-capitalize pr-1">
                    <strong> | </strong>
                    <strong>Formats: </strong>{element.formats.toString()}
                  </p>
                </div> : null}
            </div>
          </div>
          {element.sources ?
            <div className="card-list-item">
              <p className="card-text pr-1">
                <strong>Browse on Github: </strong>
                <a target="_blank" rel="noopener noreferrer" href={element.sources}>{element.sources}</a>
              </p>
            </div> : null}
          {element.sources ?
            <div className="card-list-item">
              <p className="card-text pr-1">
                <strong>Sources: </strong>
                <a target="_blank" rel="noopener noreferrer" href={element.sources}>{element.sources}</a>
              </p>
            </div> : null}
        </div>
      </div>
      <div className="d-flex flex-column justify-content-center align-items-center p-4">
        <h6>DOWNLOAD</h6>
        <a
          className="card-button"
          style={{
            pointerEvents: element.isPrivate && !authorized ? "none" : "all",
            maxWidth: "120px"
          }}
          href={`download_metadata?dataset=${element.id}`}
          download
        >
          <button className="btn btn-outline-primary">Metadata</button>
        </a>
        <div className="d-flex">
          {authIcons.map((icon, index) => <div key={"authIcon_" + index} className="p-1">{icon}</div>)}
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
  formats: PropTypes.string,
  modalities: PropTypes.string,
  sources: PropTypes.number
};

DatasetElement.defaultProps = {
  imagePath: "",
  downloadPath: ""
};

export default DatasetElement;
