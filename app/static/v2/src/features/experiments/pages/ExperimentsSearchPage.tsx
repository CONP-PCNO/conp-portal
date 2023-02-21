import React from 'react';
import { ExperimentTable } from '../components/ExperimentTable';

import { type Experiment } from '../types';

interface ExperimentsSearchPageProps {
  experiments: Experiment[];
}

export const ExperimentsSearchPage = ({ experiments }: ExperimentsSearchPageProps) => {
  return <ExperimentTable experiments={experiments} />;
};
