import { create } from 'zustand';
import { Experiment } from '../types';

interface SortKeyState {
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

interface ExperimentTableState {
  items: Experiment[];
  pagination: PaginationState;
  sortKey: SortKeyState;
  incrementCurrentPage: () => void;
  decrementCurrentPage: () => void;
  setActiveSortKey: (active: string) => void;
  setItemsPerPage: (itemsPerPage: number) => void;
}

export const useExperimentTableStore = create<ExperimentTableState>((set, get) => ({
  items: [],
  pagination: {
    currentPage: 0,
    itemsPerPage: 10
  },
  sortKey: {
    active: 'titleAsc',
    options: {
      titleAsc: {
        label: 'Title (Ascending)'
      },
      titleDesc: {
        label: 'Title (Descending)'
      }
    }
  },
  incrementCurrentPage: () => null,
  decrementCurrentPage: () => null,
  setActiveSortKey: (active) => set({ sortKey: { ...get().sortKey, active } }),
  setItemsPerPage: (itemsPerPage) => set({ pagination: { ...get().pagination, itemsPerPage } })
}));
