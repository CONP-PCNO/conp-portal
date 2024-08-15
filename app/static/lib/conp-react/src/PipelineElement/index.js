import React, { useState } from "react";
import PropTypes from "prop-types";

import ViewsIcon from "../social/ViewsIcon"
import DownloadsIcon from "../social/DownloadsIcon"
import ArkIdElement from "../ArkIdElement"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faQuestionCircle} from "@fortawesome/free-solid-svg-icons";
import ReactToolTip from "react-tooltip";
import CbrainModalPipeline from "../CbrainModalPipeline";

const PipelineElement = (props) => {
  const { authorized, ...element } = props;

  const [showCbrainTipText, setShowCbrainTipText] = useState(false);

  const [cbrainModalOpen, setCbrainModalOpen] = useState(false);

  const openCbrainModal = (datasetTitle, datasetUrl, pipelineTitle, pipelineUrl) => {
    $("#cbrainModal").modal("show");
    setCbrainModalOpen(true);
  };
  $("#cbrainModal").on("hidden.bs.modal", (event) => setCbrainModalOpen(false));

  const handleCrainMouseEnter = e => {
    setShowCbrainTipText(true);
  }

  const handleCrainMouseLeave = e => {
    setShowCbrainTipText(false);
  }

  const platforms = element.platforms.map((item, key) =>
    <div className="row w-100 align-items-center">
      <div className="col-10 p-0">
        {item.uri ?
          <button className="btn btn-outline-success m-1" onClick={openCbrainModal}>
            <div className="d-flex row align-items-center justify-content-center">
              Use This Tool On <img
              className="cbrain-img justify-content-center align-items-center pl-4"
              src="static/img/cbrain-long-logo-blue.png"
              style={{maxHeight: '30px'}}
              alt="CBRAIN logo"
            />
            </div>
          </button> :
          <button className="btn btn-outline-secondary disabled m-1">
            <div className="d-flex row align-items-center justify-content-center">
              Use This Tool On
              <img
                className="cbrain-img justify-content-center align-items-center pl-4"
                src="static/img/cbrain-long-logo-grey.png"
                style={{maxHeight: '30px'}}
                alt="Disabled CBRAIN logo"
              />
            </div>
          </button>
        }
      </div>
      <div className="col-2 p-2">
        <div className="card-text pl-1">
          <FontAwesomeIcon
            icon={faQuestionCircle}
            color="dimgray"
            size="lg"
            onMouseEnter={handleCrainMouseEnter}
            onMouseLeave={handleCrainMouseLeave}
            data-tip
            data-for="cbrainTip"
          />
          {showCbrainTipText &&
            <ReactToolTip id="cbrainTip" multiline={true} style={{ Width: "70px", WhiteSpace: "pre-wrap" }}>
              CBRAIN allows users to run analysis pipelines on a network of high-performance <br/>
              computing clusters through a friendly web-browser-based interface.
            </ReactToolTip>
          }
        </div>
      </div>
    </div>
  );

  return (
    <div className="card container-fluid" data-type="pipeline">
      <div className="row">
        <div className="col col-lg-2 d-flex flex-column p-2">
          <div className="flex-grow-1 d-flex flex-column justify-content-center align-items-center pb-3">
            <img
              alt="dataset format"
              className="img-fluid p-2"
              style={{ maxWidth: '140px' }}
              src="static/img/cogs-solid-grey.png"
            />
          </div>
          <div className="d-flex flex-grow-2 flex-row justify-content-center align-items-end">
            <ViewsIcon type="pipeline" id={element.id} />
            {element.downloads ? <DownloadsIcon type="pipeline" id={element.id} /> : null}
          </div>
        </div>

        <div className="col col-lg-7 card-body d-flex p-2">
          <div className="d-flex flex-column justify-content-center">
            <h5 className="card-title text-card-title">
              <a className="text-reset" href={`pipeline?id=${element.id}`}>
                {element.title}
              </a>
            </h5>
            <div className="py-2">
              <ul className="d-flex align-items-start">
                <li className="card-list-item">
                  <strong>Tags: </strong>{element.tags && element.tags.domain ?
                    Array.isArray(element.tags.domain) ?
                    element.tags.domain.map(tag => <span key={"tag" + tag} className="mr-1"><span className="badge badge-primary">{tag.toLowerCase()}</span></span>)
                    : <span><span className="badge badge-primary">{element.tags.domain.toLowerCase()}</span></span>
                  : null}
                </li>
              </ul>
              <ul className="d-flex align-items-start">
                <li className="card-list-item">
                  <strong>Publication Date: </strong> {element.publicationdate}
                </li>
              </ul>
              <ul className="d-flex align-items-start">
                <li className="card-list-item">
                  <strong>Description: </strong> {element.description}
                </li>
              </ul>
              <ul className="d-flex align-items-start">
                <li className="card-list-item">
                  <strong>Pipeline ID: </strong>
                  <a
                    target="_blank"
                    rel="noopener noreferrer"
                    href={"https://www.zenodo.org/record/" + element.id.split(".")[1]}
                  >
                    {element.id}
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <ArkIdElement id={element.ark_id}/>
            </div>
          </div>
        </div>

        <div className="col col-lg-3 d-flex flex-column justify-content-center align-items-end p-2">
          <div className="row align-items-center w-100">

            {platforms}
          </div>
        </div>
      </div>
      {cbrainModalOpen ? (
        <CbrainModalPipeline
          platforms={element.platforms}
          title={element.title}
          cbrainIds={element.cbrainIds}
        />
      ) : null}
    </div>
  );
};

PipelineElement.propTypes = {
  id: PropTypes.string,
  title: PropTypes.string,
  description: PropTypes.string,
  downloads: PropTypes.number,
  publicationdate: PropTypes.string,
  descriptorurl: PropTypes.string,
  platforms: PropTypes.arrayOf(PropTypes.object),
  name: PropTypes.string,
  commandline: PropTypes.string,
  author: PropTypes.string,
  inputs: PropTypes.arrayOf(PropTypes.object),
  outputfiles: PropTypes.arrayOf(PropTypes.object),
  toolversion: PropTypes.string,
  schemaversion: PropTypes.string,
  containerimage: PropTypes.object,
  tags: PropTypes.object,
  url: PropTypes.string,
  img: PropTypes.string,
  imagePath: PropTypes.string,
  cbrainIds: PropTypes.arrayOf(PropTypes.Object),
};

export default PipelineElement;
