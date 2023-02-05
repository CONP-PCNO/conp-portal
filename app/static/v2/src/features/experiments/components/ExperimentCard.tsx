import React from 'react';

import brain from '@/assets/brain.gif';
import { type Experiment } from '../types';
import { ExperimentCardItem } from './ExperimentCardItem';

interface ExperimentCardProps {
  titleLink?: boolean;
  experiment: Experiment;
}

export const ExperimentCard = ({
  titleLink,
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
    repositorySize
  }
}: ExperimentCardProps) => {
  return (
    <div className="card container-fluid">
      <div className="row">
        <div className="col col-sm-2 d-flex flex-column justify-content-center">
          <div className="container-fluid p-2">
            <img className="animated-gif img-fluid" alt="experiment image" src={imageFile || brain} />
          </div>
        </div>
        <div className="col col-lg-7 card-body d-flex p-2">
          <div className="d-flex flex-column justify-content-center">
            <h5 className="card-title text-card-title">
              {titleLink ? (
                <a className="text-reset" href="#">
                  {title}
                </a>
              ) : (
                <span className="text-reset">{title}</span>
              )}
            </h5>
            <div>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Creators" value={creators} />
                <ExperimentCardItem label="Description" value={description} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Version" value={version} />
                <ExperimentCardItem label="Date Added" value={dateAdded} />
                <ExperimentCardItem label="Date Updated" value={dateUpdated} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Modalities" value={modalities} />
                <ExperimentCardItem label="Primary Software" value={primarySoftware} />
                <ExperimentCardItem label="Primary Function" value={primaryFunction} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="DOI" value={doi} />
              </ul>
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="License" value={license} />
              </ul>
            </div>
            <div className="py-1">
              <ul className="d-flex align-items-start">
                <ExperimentCardItem label="Files" value={repositoryFileCount} />
                <ExperimentCardItem label="Size" value={repositorySize} />
              </ul>
            </div>
          </div>
        </div>
        <div className="col col-lg-3 p-2">
          <div className="container-fluid d-flex flex-column justify-content-center h-100">
            <div className="d-flex flex-column align-items-center my-2">
              <i className="fa fa-eye fa-2x" aria-hidden="true"></i>
              {views}
            </div>
            <div className="d-flex flex-column align-items-center">
              <i className="fa fa-download fa-2x" aria-hidden="true"></i>
              {downloads}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
