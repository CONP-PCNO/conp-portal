import React, { useMemo, useState } from 'react';

import { Dropdowns } from './Dropdowns';
import { SearchBar, SearchFilters } from './SearchBar';

import { type Experiment } from '@/features/experiments/types';
import { ExperimentCard } from '@/features/experiments/components/ExperimentCard';
import { ExperimentTableContext } from '../../context/ExperimentTableContext';
import { PaginationNav } from './PaginationNav';

const sortKeyOptions = {
  titleAsc: {
    label: 'Title (Ascending)',
    key: 'title',
    method: 'ascending'
  },
  titleDesc: {
    label: 'Title (Descending)',
    key: 'title',
    method: 'descending'
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

  const totalItems = experiments.length;

  // Filter
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
    [experiments]
  );

  // Sort
  experiments = experiments.sort((a, b) => {
    const { key, method } = sortKeyOptions[activeSortKey];
    return method === 'ascending' ? (a[key] > b[key] ? 1 : -1) : a[key] < b[key] ? 1 : -1;
  });

  // Pagination
  const firstItemIndex = currentPage * itemsPerPage;
  const lastItemIndex = Math.min(firstItemIndex + itemsPerPage, experiments.length);
  experiments = experiments.slice(firstItemIndex, lastItemIndex);

  return (
    <ExperimentTableContext.Provider
      value={{
        items: experiments,
        pagination: {
          currentPage,
          itemsPerPage,
          firstItemIndex,
          lastItemIndex,
          totalItems
        },
        sortKey: {
          active: activeSortKey,
          options: sortKeyOptions
        },
        setActiveSortKey: (active) => setActiveSortKey(active as SortKeyOptions),
        setCurrentPage: setCurrentPage,
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
      <PaginationNav />
    </ExperimentTableContext.Provider>
  );
};
