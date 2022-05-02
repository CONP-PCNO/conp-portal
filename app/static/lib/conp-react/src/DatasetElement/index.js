import React, { useState } from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserLock } from '@fortawesome/free-solid-svg-icons'
import { faUserAlt } from '@fortawesome/free-solid-svg-icons'

import ViewsIcon from '../social/ViewsIcon'
import DownloadsIcon from '../social/DownloadsIcon'
import ArkIdElement from '../ArkIdElement'
import DownloadModalWindowElement from './DownloadModalWindowElement'

const DatasetElement = props => {
  const { authorized, imagePath, ...element } = props;

  const [downloadModalOpen, setDownloadModalOpen] = useState(false);

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

  const openDownloadModal = () => {
    $("#downloadModal").modal("show");
    setDownloadModalOpen(true);
  };
  $("#downloadModal").on("hidden.bd.modal", (event) => setDownloadModalOpen(false))

  return (
    <div className="card container-fluid" data-type="dataset">
      <div className="row">
        <div className="col col-lg-2 d-flex flex-column p-2">
          <div className="flex-grow-2 d-flex flex-column justify-content-center align-items-center">
            <img
                alt="dataset format"
                className="img-fluid w-100"
                style={{maxWidth: '180px'}}
                src={element.logoFilepath.startsWith('http') ? element.logoFilepath : element.thumbnailURL}
            />
          </div>
          <div className="flex-grow-1 d-flex flex-row align-items-end">
            {element.conpStatus !== 'external' ? (<img height="36" width="36" src={statusCONP} alt="CONP status"/>) :
                <div style={{width: 36}}/>}
            <ViewsIcon type="dataset" id={element.id}/>
            <DownloadsIcon type="dataset" id={element.id + "_version-" + element.version + '.tar.gz'}/>
          </div>
        </div>
        <div className="col col-lg-7 card-body d-flex p-2">
          <div className="d-flex flex-column justify-content-center">
            <h5 className="card-title text-card-title">
              <a className="text-reset" href={`dataset?id=${element.id}`}>
                {element.title}
              </a>
            </h5>
            <div className="py-2">
              <ul className="d-flex align-items-start">
                {element.creators ?
                    <li className="card-list-item">
                      <strong>Creators: </strong>{element.creators.length > 3 ? element.creators.slice(0, 3).join(', ') + ' et al.' : element.creators.join(', ')}
                    </li> : null}
                {element.origin?.institution ?
                    <li className="card-list-item">
                      <strong>Institution: </strong>{element.origin.institution}
                    </li> : null}
                {element.origin?.consortium ?
                    <li className="card-list-item">
                      <strong>Consortium: </strong>{element.origin.consortium}
                    </li> : null}
              </ul>
              <ul className="d-flex align-items-start">
                {element.version ?
                    <li className="card-list-item">
                      <strong>Version: </strong>{element.version}
                    </li> : null}
                {element.dateAdded ?
                    <li className="card-list-item">
                      <strong>Date Added: </strong>{element.dateAdded}
                    </li> : null}
                {element.dateUpdated ?
                    <li className="card-list-item">
                      <strong>Date Updated: </strong>{element.dateUpdated}
                    </li> : null}
              </ul>
              <ul className="d-flex align-items-start">
                {element.types ?
                    <li className="card-list-item">
                      <strong>Data Types: </strong>{element.types}
                    </li> : null}
                {element.modalities ?
                    <li className="card-list-item">
                      <strong>Modalities: </strong>{element.modalities.join(', ')}
                    </li> : null}
                {element.licenses ?
                    <li className="card-list-item">
                      <strong>License: </strong>{element.licenses}
                    </li> : null}
              </ul>
              <ul className="d-flex align-items-start">
                {element.files ?
                    <li className="card-list-item">
                      <strong>Files: </strong>{element.files}
                    </li> : null}
                {element.size ?
                    <li className="card-list-item">
                      <strong>Size: </strong>{element.size}
                    </li> : null}
                {element.subjects ?
                    <li className="card-list-item">
                      <strong>Subjects: </strong>{element.subjects}
                    </li> : null}
                {element.formats ?
                    <li className="card-list-item">
                      <strong>Formats: </strong>{element.formats.join(', ')}
                    </li> : null}
              </ul>
            </div>
            <div>
              <ArkIdElement id={element.ark_id}/>
            </div>
          </div>
        </div>
        <div className="col col-lg-3 d-flex flex-column justify-content-center align-items-center p-2">
          <div className="col align-items-center justify-content-center width-auto">

            <div className="row justify-content-center align-items-center p-2">
              <h7><strong>DOWNLOAD OPTIONS</strong></h7>
            </div>
            <div className="col justify-content-center align-items-center">
              {element.showDownloadButton ?
                <button type="button" className="btn btn-outline-success m-1" onClick={() => openDownloadModal()}>
                  Archived Dataset ({element.size})
                </button> :
                <button type="button" className="btn btn-outline-secondary m-1 disabled">
                  Archived Dataset (Not Available)
                </button>
              }
              <a href={`dataset?id=${element.id}#dataladInstructions`} role="button"
                   className="btn btn-outline-success m-1">
                DataLad Instructions
              </a>
            </div>
            <div className="d-flex justify-content-center align-items-center">
              {authIcons.map((icon, index) => <div key={"authIcon_" + index}
                                                   className="text-center p-1">{icon}</div>)}
            </div>

            <div className="row justify-content-center align-items-center p-2">
              <h7><strong>PROCESS ON</strong></h7>
            </div>
            <div className="row justify-content-center align-items-center">
              {element.cbrain_id ?
                  <a target="_blank" href={`${element.cbrain_id}`}>
                    <img
                        className="cbrain-img justify-content-center align-items-center"
                        src="static/img/cbrain-long-logo-blue.png" style={{maxHeight: '50px'}}/>
                  </a> :
                  <a target="_blank">
                    <img
                        className="cbrain-img justify-content-center align-items-center"
                        src="static/img/cbrain-long-logo-grey.png" style={{maxHeight: '50px'}}/>
                  </a>}
            </div>
          </div>
        </div>
      </div>
      {downloadModalOpen ? <DownloadModalWindowElement {...props} /> : null}
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
  sources: PropTypes.number,
  cbrain_id: PropTypes.string,
  ark_id: PropTypes.string,
  zipLocation: PropTypes.string,
  showDownloadButton: PropTypes.bool
};

DatasetElement.defaultProps = {
  imagePath: "",
  downloadPath: ""
};

export default DatasetElement;
