import React, { useState } from 'react';

import { Dropdowns } from './Dropdowns';
import { SearchBar } from './SearchBar';

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

  // Filter

  const [searchFilters, setSearchFilters] = useState(() => {
    const filters = {
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
    };
    return Object.fromEntries(
      Object.entries(filters).map(([key, { label, options }]) => {
        return [key, { label, options: Object.fromEntries(options.map((option) => [option, false])) }];
      })
    );
  });

  /*
  Object.entries(searchFilters).forEach(([filter, { options }]) => {
    Object.entries(options).forEach(([key, value]) => {
      if (value) {
        // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
        experiments = experiments.filter((e) => e[filter][key])
      }
      console.log(filter, key, value)
    })
  }); */

  const totalItems = experiments.length;
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
        searchFilters,
        toggleSearchFilter: (filter, option, isActive) => {
          setSearchFilters((prevState) => ({ ...prevState, [filter]: { ...prevState[filter], [option]: isActive } }));
        },
        setActiveSortKey: (active) => setActiveSortKey(active as SortKeyOptions),
        setCurrentPage: setCurrentPage,
        setItemsPerPage: setItemsPerPage
      }}
    >
      <SearchBar />
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
