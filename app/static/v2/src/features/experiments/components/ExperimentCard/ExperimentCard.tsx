import React from 'react';

import brain from '@/assets/brain.gif';
import { type Experiment } from '@/features/experiments/types';
import { ExperimentCardItem } from './ExperimentCardItem';

import ReactFreezeframe from 'react-freezeframe';

interface ExperimentCardProps {
  titleLink?: string;
  downloadLink: string;
  experiment: Experiment;
}

const getPlatformFromUrl = (url: string): string => {
  const match = url.match(/https:\/\/(.*?)\.[a-z]+\/?/);
  if (!match) return "";

  // Capture le terme de la plateforme et met la première lettre en majuscule
  const platform = match[1];
  return platform.charAt(0).toUpperCase() + platform.slice(1);
};


export const ExperimentCard = ({
  titleLink,
  downloadLink,
  experiment: {
    title,
    description,
    creators,
    version,
    dateAdded,
    dateUpdated,
    license,
    modalities,
    primarySoftware,
    primaryFunction,
    doi,
    views,
    downloads,
    imageFile,
    repositoryFileCount,
    repositorySize,
    id,
    remoteUrl,
    source
  }
}: ExperimentCardProps) => {
  return (
    <div className="card container-fluid">
      <div className="row">
        <div className="col col-sm-2 d-flex flex-column justify-content-center">
          <div className="container-fluid p-2">
            <ReactFreezeframe className="animated-gif img-fluid" alt="experiment image" src={`/experiments/experiment_logo/${id}`} />
          </div>
          <div className='flex-grow-2 d-flex fex-row justify-content-center align-items-end'>
            <div className="d-flex flex-column align-items-center mx-2">
              <i className="fa fa-eye fa-lg" aria-hidden="true"></i>
                {views.toString() === "" ? "N/A" : views}
            </div>
            <div className="d-flex flex-column align-items-center mx-2">
              <i className="fa fa-download fa-lg" aria-hidden="true"></i>
                {downloads.toString() === "" ? "N/A" : downloads}
            </div>
          </div>
        </div>
        <div className="col col-lg-7 card-body d-flex p-2">
          <div className="d-flex flex-column justify-content-center">
            <h5 className="card-title text-card-title">
              {titleLink ? (
                <a className="text-reset" href={titleLink}>
                  {title}
                </a>
              ) : (
                <span className="text-reset">{title}</span>
              )}
            </h5>
            <div>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Creators" value={creators} />
                {/* <ExperimentCardItem label="Description" value={description} /> */}
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Version" value={version} />
                <ExperimentCardItem label="Date Added" value={dateAdded} />
                <ExperimentCardItem label="Date Updated" value={dateUpdated} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Modalities" value={modalities} />
                <ExperimentCardItem label="License" value={license} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="DOI" value={doi} />
                <ExperimentCardItem label="Primary Software" value={primarySoftware} />
                <ExperimentCardItem label="Primary Function" value={primaryFunction} />
              </ul>
              {/* <ul className="d-flex align-items-start">
                <ExperimentCardItem label="License" value={license} />
              </ul> */}
            </div>
            <div className="py-1">
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Files" value={repositoryFileCount} />
                <ExperimentCardItem label="Size" value={repositorySize} />
              </ul>
            </div>
          </div>
        </div>
        <div className="col col-lg-3 d-flex felx-column justify-content-center align-items-center p-2">
            <div className="row align-items-center w-100">
              <div className='col-10 p-0'>
              <a className="btn btn-success mb-2" role='button' href={downloadLink}>
                Download This Experiment
              </a>
              {/* <a className="btn btn-success" role='button' href={source}>
                View From {getPlatformFromUrl(source)}
              </a> */}
              </div>
            </div>
        </div>
      </div>
    </div>
  );
};
