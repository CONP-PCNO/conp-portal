import React, { useMemo, useState } from 'react';

import { Dropdowns } from './Dropdowns';
import { SearchBar, SearchFilters } from './SearchBar';

import { type Experiment } from '@/features/experiments/types';
import { ExperimentCard } from '@/features/experiments/components/ExperimentCard';
import { useExperimentTableStore } from '@/features/experiments/store/experiment-table-store';

interface ExperimentTableProps {
  experiments: Experiment[];
}

export const ExperimentTable = ({ experiments }: ExperimentTableProps) => {
  const store = useExperimentTableStore();

  const filters: SearchFilters = useMemo(
    () => ({
      modalities: {
        label: 'Modalities',
        options: Array.from(new Set(experiments.flatMap((item) => item.modalities)))
      },
      primaryFunction: {
        label: 'Primary Function',
        options: Array.from(new Set(experiments.flatMap((item) => item.primaryFunction)))
      },
      primarySoftware: {
        label: 'Primary Software',
        options: Array.from(new Set(experiments.flatMap((item) => item.primarySoftware)))
      }
    }),
    []
  );

  return (
    <div>
      <SearchBar filters={filters} />
      <Dropdowns />
      <div className="search-dataset-table">
        {experiments.map((experiment) => (
          <ExperimentCard key={experiment.id} experiment={experiment} />
        ))}
      </div>
    </div>
  );
};
