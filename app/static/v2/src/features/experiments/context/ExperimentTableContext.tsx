import { createContext } from 'react';

import { type Experiment } from '@/features/experiments/types';

export interface SortKeyState {
  active: string;
  options: {
    [key: string]: {
      label: string;
      key: keyof Experiment;
      method: 'ascending' | 'descending';
    };
  };
}

export interface PaginationState {
  currentPage: number;
  itemsPerPage: number;
  firstItemIndex: number;
  lastItemIndex: number;
  totalItems: number;
}

export interface SearchFilters {
  [key: string]: {
    label: string;
    options: Record<string, boolean>;
  };
}

export interface ExperimentTableContextInterface {
  items: Experiment[];
  pagination: PaginationState;
  sortKey: SortKeyState;
  searchFilters: SearchFilters;
  toggleSearchFilter: (filter: string, option: string, isActive: boolean) => void;
  setActiveSortKey: (active: string) => void;
  setCurrentPage: (currentPage: number) => void;
  setItemsPerPage: (itemsPerPage: number) => void;
}

export const ExperimentTableContext = createContext<ExperimentTableContextInterface | undefined>(undefined);
