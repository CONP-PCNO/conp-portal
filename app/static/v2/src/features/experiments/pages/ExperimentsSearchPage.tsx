import React from 'react';
import { ExperimentTable } from '../components/ExperimentTable';

import { type Experiment } from '../types';

interface ExperimentsSearchPageProps {
  experiments: Experiment[];
  keyword: string;
}

export const ExperimentsSearchPage = ({ experiments, keyword }: ExperimentsSearchPageProps) => {
  return <ExperimentTable experiments={experiments} keyword={keyword} />;
};
