import React from 'react';

import { SearchBar, type SearchFilters } from '@/components/SearchBar';

interface ExperimentsSearchPageProps {
  filters: SearchFilters
}

export const ExperimentsSearchPage = ({ filters }: ExperimentsSearchPageProps) => {
  return (
    <div className="search-dataset-table">
      <SearchBar filters={filters} onSubmit={() => console.log("experiments.handleSubmitSearch(event)")} />
    </div>
  )
}