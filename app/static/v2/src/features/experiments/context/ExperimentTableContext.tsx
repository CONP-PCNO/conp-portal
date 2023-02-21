import { createContext } from 'react';

import { type Experiment } from '@/features/experiments/types';

export interface SortKeyState {
  active: string;
  options: {
    [key: string]: {
      label: string;
    };
  };
}

export interface PaginationState {
  currentPage: number;
  itemsPerPage: number;
}

export interface ExperimentTableContextInterface {
  items: Experiment[];
  pagination: PaginationState;
  sortKey: SortKeyState;
  incrementCurrentPage: () => void;
  decrementCurrentPage: () => void;
  setActiveSortKey: (active: string) => void;
  setItemsPerPage: (itemsPerPage: number) => void;
}

export const ExperimentTableContext = createContext<ExperimentTableContextInterface | undefined>(undefined);
