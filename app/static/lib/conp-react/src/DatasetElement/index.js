import React, { useState } from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserLock } from "@fortawesome/free-solid-svg-icons";
import { faUserAlt } from "@fortawesome/free-solid-svg-icons";

import ViewsIcon from '../social/ViewsIcon'
import DownloadsIcon from '../social/DownloadsIcon'
import ArkIdElement from "../ArkIdElement"
import CbrainModalDataset from "../CbrainModalDataset";

const DatasetElement = (props) => {
  const { authorized, imagePath, ...element } = props;

  const [metadataSpinnerState, setMetadataSpinnerState] = useState(false);
  const [datasetSpinnerState, setDatasetSpinnerState] = useState(false);

  const [metadataErrorState, setMetadataErrorState] = useState(false);
  const [datasetErrorState, setDatasetErrorState] = useState(false);

  const [metadataErrorText, setMetadataErrorText] = useState("");
  const [datasetErrorText, setDatasetErrorText] = useState("");

  const [modalOpen, setModalOpen] = useState(false);

  const statusCONP = `${imagePath}/canada.svg`;

  let authIcons = [];
  switch (element.authorizations) {
    case "restricted":
      authIcons.push(
        <span>
          <FontAwesomeIcon icon={faUserAlt} color="dimgray" size="lg" /> - CONP
          account required
        </span>
      );
      break;
    case "private":
      authIcons.push(
        <span>
          <FontAwesomeIcon icon={faUserLock} color="dimgray" size="lg" /> -
          Third-party account required
        </span>
      );
      break;
    default:
      break;
  }

  const downloadMetadata = (event) => {
    setMetadataSpinnerState(true);
    setMetadataErrorState(false);

    fetch(`${window.origin}/download_metadata?dataset=${element.id}`)
      .then((response) => {
        if (response.ok) {
          return response.blob();
        } else {
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
      })
      .then(function (blob) {
        var file = window.URL.createObjectURL(blob, {
          type: "application/json",
        });
        let link = document.createElement("a");
        link.href = file;
        link.download = `${element.title
          .toLowerCase()
          .replace(" ", "_")}.dats.json`;
        link.click();

        // For Firefox it is necessary to delay revoking the ObjectURL.
        setTimeout(() => {
          window.URL.revokeObjectURL(file);
        }, 250);
      })
      .catch(function (error) {
        setMetadataErrorState(true);
        setMetadataErrorText(
          `Something went wrong when trying to download the metadata: ${error}`
        );
      })
      .finally(function () {
        setMetadataSpinnerState(false);
      });
  };

  const downloadDataset = (event) => {
    setDatasetSpinnerState(true);
    setDatasetErrorState(false);

    fetch(
      `${window.origin}/download_content?id=${element.id}&version=${element.version}`
    )
      .then((response) => {
        if (response.ok) {
          return response.blob();
        } else {
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
      })
      .then(function (blob) {
        var file = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = file;
        a.download = "{{ data.title }}.{{ metadata.version }}.tar.gz";
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch(function (error) {
        setDatasetErrorState(true);
        setDatasetErrorText(
          `Something went wrong when trying to download this dataset: ${error}`
        );
      })
      .finally(function () {
        setDatasetSpinnerState(false);
      });
  };

  const openModal = () => {
    $("#cbrainModal").modal("show");
    setModalOpen(true);
  };
  $("#cbrainModal").on("hidden.bs.modal", (event) => setModalOpen(false))

  return (
    <>
      <div className="card container-fluid" data-type="dataset">
        <div className="row pr-4">
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
          <div className="col col-lg-7 card-body d-flex">
            <div className="d-flex flex-column justify-content-center p-2">
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
          <div className="col col-lg-3 d-flex flex-column justify-content-top align-items-center pr-2">
            <div className="row align-items-top width-auto">

              <div className="col col-lg-6 d-flex flex-column justify-content-top align-items-center p-2 pr-4">
                <h7><strong>PROCESS</strong></h7>
                  {element.cbrain_id ? (
                    <>
                      <button className="btn" onClick={openModal}>
                        <img
                          className="cbrain-img"
                          src="static/img/cbrain-icon-blue.png"
                          style={{ maxWidth: "60px" }}
                          alt="Open Dataset"
                        />
                      </button>
                    </>
                  ) : (
                    <>
                      <img
                          alt="Dataset not available on CBRAIN"
                          className="cbrain-img justify-content-center align-items-center"
                          src="static/img/cbrain-icon-grey.png"
                          style={{ maxWidth: "60px" }}
                      />
                    </>
                  )}
              </div>
              <div className="col col-lg-6 d-flex flex-column justify-content-top align-items-center p-2">
                <h7><strong>DOWNLOAD</strong></h7>
                <div className="d-flex flex-column">
                  <button type="button" className="btn btn-outline-secondary m-1" onClick={() => downloadMetadata()}>
                    Metadata
                    <div className="spinner-border text-primary" role="status" hidden={!metadataSpinnerState}>
                      <span className="sr-only">Loading...</span>
                    </div>
                  </button>
                  <div className="alert alert-danger" role="alert" hidden={!metadataErrorState}>
                    {metadataErrorText}
                  </div>
                  <a href={`dataset?id=${element.id}#downloadInstructions`} role="button"
                     className="btn btn-outline-secondary m-1">
                    Dataset
                    <div className="spinner-border text-primary" role="status" hidden={!datasetSpinnerState}>
                      <span className="sr-only">Loading...</span>
                    </div>
                  </a>
                  <div className="alert alert-danger" role="alert" hidden={!datasetErrorState}>
                    {datasetErrorText}
                  </div>
                </div>
                <div className="d-flex">
                  {authIcons.map((icon, index) => <div key={"authIcon_" + index}
                                                       className="text-center p-1">{icon}</div>)}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {modalOpen ? (
        <CbrainModalDataset
          title={element.title}
          cbrainIds={element.cbrainIds}
          cbrain_id={element.cbrain_id}
        />
      ): null}
    </>
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
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
  ark_id: PropTypes.string,
};

DatasetElement.defaultProps = {
  imagePath: "",
  downloadPath: "",
};

export default DatasetElement;
