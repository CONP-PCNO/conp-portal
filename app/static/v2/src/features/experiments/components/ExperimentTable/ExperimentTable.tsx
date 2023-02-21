import React, { useMemo, useState } from 'react';

import { Dropdowns } from './Dropdowns';
import { SearchBar, SearchFilters } from './SearchBar';

import { type Experiment } from '@/features/experiments/types';
import { ExperimentCard } from '@/features/experiments/components/ExperimentCard';
import { ExperimentTableContext } from '../../context/ExperimentTableContext';

const sortKeyOptions = {
  titleAsc: {
    label: 'Title (Ascending)'
  },
  titleDesc: {
    label: 'Title (Descending)'
  }
} as const;

type SortKeyOptions = keyof typeof sortKeyOptions;

interface ExperimentTableProps {
  experiments: Experiment[];
}

export const ExperimentTable = ({ experiments }: ExperimentTableProps) => {
  const [activeSortKey, setActiveSortKey] = useState<SortKeyOptions>('titleAsc');
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(10);

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
    <ExperimentTableContext.Provider
      value={{
        items: experiments,
        pagination: {
          currentPage: currentPage,
          itemsPerPage: itemsPerPage
        },
        sortKey: {
          active: activeSortKey,
          options: sortKeyOptions
        },
        incrementCurrentPage: () => null,
        decrementCurrentPage: () => null,
        setActiveSortKey: (active) => setActiveSortKey(active as SortKeyOptions),
        setItemsPerPage: setItemsPerPage
      }}
    >
      <SearchBar filters={filters} />
      <Dropdowns />
      <div className="search-dataset-table">
        {experiments.map((experiment) => (
          <ExperimentCard key={experiment.id} experiment={experiment} />
        ))}
      </div>
    </ExperimentTableContext.Provider>
  );
};
