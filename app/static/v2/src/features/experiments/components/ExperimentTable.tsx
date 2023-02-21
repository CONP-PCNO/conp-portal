import React, { useMemo, useState } from 'react';

import { Dropdowns } from '@/components/Dropdowns';
import { type Pagination, type SortKeyOptions } from '@/components/Dropdowns';
import { SearchBar, SearchFilters } from '@/components/SearchBar';

import { type Experiment } from '../types';
import { ExperimentCard } from './ExperimentCard';

interface ExperimentTableProps {
  experiments: Experiment[];
}

export const ExperimentTable = ({ experiments }: ExperimentTableProps) => {
  const [activeSortKey, setActiveSortKey] = useState('title');

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

  const pagination: Pagination = {
    currentPage: 1,
    itemsPerPage: 10,
    totalItems: experiments.length
  };

  const sortKeyOptions: SortKeyOptions = {
    title: {
      label: 'Title'
    }
  };

  const handlePerPageChange = (perPage: number) => {
    alert(`Setting per page: ${perPage}`);
  };

  const handleSortKeySelection = (sortKey: string) => {
    alert(`Setting sort key: ${sortKey}`);
  };

  return (
    <div>
      <SearchBar filters={filters} />
      <Dropdowns
        activeSortKey={activeSortKey}
        sortKeyOptions={sortKeyOptions}
        pagination={pagination}
        onPerPageSelection={handlePerPageChange}
        onSortKeySelection={handleSortKeySelection}
      />
      <div className="search-dataset-table">
        {experiments.map((experiment) => (
          <ExperimentCard key={experiment.id} experiment={experiment} />
        ))}
      </div>
    </div>
  );
};
