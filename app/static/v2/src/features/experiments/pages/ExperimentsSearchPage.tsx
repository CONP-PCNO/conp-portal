import React from 'react';
import { ExperimentCard } from '../components/ExperimentCard';

import { type Experiment } from '../types';

interface ExperimentsSearchPageProps {
  experiments: Experiment[]
}

export const ExperimentsSearchPage = ({ experiments }: ExperimentsSearchPageProps) => {
  console.log(experiments)
  return (
    <div className="search-dataset-table">
      {experiments.map((experiment) => <ExperimentCard key={experiment.id} experiment={experiment} /> )}
    </div>
  )
}