import React from 'react';

import { ExperimentCard } from '../components/ExperimentCard';
import { Experiment } from '../types';

const additionalProps: Array<keyof Experiment> = [
  'origin',
  'contactPerson',
  'contactEmail',
  'privacy',
  'keywords',
  'otherSoftware',
  'otherFunctions',
  'acknowledgements',
  'source'
];

export interface ExperimentPageProps {
  experiment: Experiment;
  downloadLink: string;
}

export const ExperimentPage = ({ experiment, downloadLink }: ExperimentPageProps) => {
  return (
    <div>
      <ExperimentCard experiment={experiment} />
      <a className="btn btn-primary text-white mt-3" href={downloadLink}>
        Download This Experiment
      </a>
      <h3>Additional Information</h3>
      <ul>
        {additionalProps.map((prop) => (
          <li key={prop}>
            {prop}: {experiment[prop] || 'NA'}
          </li>
        ))}
      </ul>
    </div>
  );
};
