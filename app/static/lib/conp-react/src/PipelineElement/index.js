import React, { useState, useRef, useLayoutEffect } from "react";
import PropTypes from "prop-types";

import ViewsIcon from "../social/ViewsIcon"
import DownloadsIcon from "../social/DownloadsIcon"
import ArkIdElement from "../ArkIdElement"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faQuestionCircle} from "@fortawesome/free-solid-svg-icons";
import ReactToolTip from "react-tooltip";
import CbrainModalPipeline from "../CbrainModalPipeline";

// A long description shows six lines, fades out over the next two, and
// offers "more" to reveal the rest. The look lives in conp-theme.css
// (.tool-description), so it can be tuned without rebuilding this bundle.
const ToolDescription = ({ text, id }) => {
  const ref = useRef(null);
  const [expanded, setExpanded] = useState(false);
  const [overflows, setOverflows] = useState(false);

  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const measure = () => {
      if (!el.classList.contains("is-clamped")) {
        el.classList.add("is-clamped");
        setOverflows(el.scrollHeight > el.clientHeight + 1);
        el.classList.remove("is-clamped");
      }
    };
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, [text]);

  if (!text) return null;
  const clamped = overflows && !expanded;
  const textId = `tool-description-${id}`;
  return (
    <div className="tool-description-wrap">
      <div
        id={textId}
        ref={ref}
        className={"tool-description" + (clamped ? " is-clamped" : "")}
        data-testid="tool-description"
      >
        {text}
      </div>
      {overflows ?
        <button
          type="button"
          className="tool-description-toggle"
          aria-expanded={expanded}
          aria-controls={textId}
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? "less" : "more"}
        </button>
        : null}
    </div>
  );
};

const PipelineElement = (props) => {
  const { authorized, ...element } = props;

  const [showCbrainTipText, setShowCbrainTipText] = useState(false);

  const [cbrainModalOpen, setCbrainModalOpen] = useState(false);

  const openCbrainModal = (datasetTitle, datasetUrl, pipelineTitle, pipelineUrl) => {
    var modalEl = document.getElementById('cbrainModal');
    if (modalEl && window.bootstrap) {
      bootstrap.Modal.getOrCreateInstance(modalEl).show();
    }
    setCbrainModalOpen(true);
  };
  var _cbrainModalEl = typeof document !== 'undefined' ? document.getElementById('cbrainModal') : null;
  if (_cbrainModalEl) {
    _cbrainModalEl.addEventListener('hidden.bs.modal', function () { setCbrainModalOpen(false); });
  }

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
            Use On <img
              className="cbrain-img justify-content-center align-items-center ps-2"
              src="static/img/cbrain-long-logo-blue.png"
              style={{maxHeight: '30px'}}
              alt="CBRAIN logo"
            />
          </button> :
          <button className="btn btn-outline-secondary disabled m-1">
            Use On
            <img
              className="cbrain-img justify-content-center align-items-center ps-2"
              src="static/img/cbrain-long-logo-grey.png"
              style={{maxHeight: '30px'}}
              alt="Disabled CBRAIN logo"
            />
          </button>
        }
      </div>
      <div className="col-2 p-2">
        <div className="card-text ps-1">
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
              alt={element.icon ? `${element.icon.label} logo` : "Tool"}
              title={element.icon ? element.icon.label : undefined}
              className="img-fluid p-2"
              data-testid="tool-icon"
              style={{ maxWidth: '140px', maxHeight: '112px', width: 'auto', height: 'auto', objectFit: 'contain' }}
              src={element.icon ? element.icon.src : "static/img/cogs-solid-grey.png"}
            />
          </div>
          <div className="d-flex flex-grow-2 flex-row justify-content-center align-items-end">
            <ViewsIcon type="pipeline" id={element.id} />
            {element.downloads ? <DownloadsIcon type="pipeline" id={element.id} /> : null}
          </div>
        </div>

        <div className="col col-lg-7 card-body d-flex p-2" style={{ minWidth: 0 }}>
          <div className="d-flex flex-column justify-content-center" style={{ minWidth: 0, width: "100%" }}>
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
                    element.tags.domain.map(tag => <span key={"tag" + tag} className="me-1"><span className="badge bg-primary">{tag.toLowerCase()}</span></span>)
                    : <span><span className="badge bg-primary">{element.tags.domain.toLowerCase()}</span></span>
                  : null}
                </li>
              </ul>
              <ul className="d-flex align-items-start">
                <li className="card-list-item">
                  <strong>Publication Date: </strong> {element.publicationdate}
                </li>
              </ul>
              <ul className="d-flex align-items-start">
                <li className="card-list-item tool-description-item">
                  <strong>Description: </strong>
                  <ToolDescription text={element.description} id={element.id} />
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
          {element.cbrain ?
            <div className="row w-100 pt-1">
              <small className="text-muted" data-testid="cbrain-versions">
                {element.cbrain.versions && element.cbrain.versions.length > 0 ?
                  <span>Runs on CBRAIN: {element.cbrain.software} {element.cbrain.versions.join(", ")}</span>
                  : <span>Runs on CBRAIN (version not stated)</span>}
                {!(element.platforms && element.platforms[0] && element.platforms[0].uri) ?
                  <span>{" · "}
                    <a
                      href="https://portal.cbrain.mcgill.ca/available"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      find it on CBRAIN
                    </a>
                  </span>
                  : null}
              </small>
            </div>
            : null}
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
  icon: PropTypes.shape({
    src: PropTypes.string,
    label: PropTypes.string
  }),
  cbrain: PropTypes.shape({
    tool: PropTypes.string,
    software: PropTypes.string,
    versions: PropTypes.arrayOf(PropTypes.string)
  }),
};

export default PipelineElement;
