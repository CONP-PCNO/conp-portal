import React from 'react';

import { SearchBar, type SearchFilters } from '@/components/SearchBar';

interface ExperimentsSearchPageProps {
  filters: SearchFilters;
  experiments: unknown
}

export const ExperimentsSearchPage = ({ filters, experiments }: ExperimentsSearchPageProps) => {
  console.log(experiments)
  return (
    <div className="search-dataset-table">
      <SearchBar filters={filters} onSubmit={() => console.log("experiments.handleSubmitSearch(event)")} />
    </div>
  )
}