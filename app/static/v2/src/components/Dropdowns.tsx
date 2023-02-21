import React from 'react';

export interface SortKeyOptions {
  [key: string]: {
    label: string;
  };
}

export interface Pagination {
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
}

export interface DropdownsProps {
  activeSortKey: keyof SortKeyOptions;
  sortKeyOptions: SortKeyOptions;
  pagination: Pagination;
  perPageOptions?: number[];
  onPerPageSelection: (perPage: number) => void;
  onSortKeySelection: (sortKey: string) => void;
}

export const Dropdowns = ({
  activeSortKey,
  sortKeyOptions,
  pagination,
  perPageOptions = [5, 10, 15, 20],
  onSortKeySelection,
  onPerPageSelection
}: DropdownsProps) => {
  const firstResultNumber = (pagination.currentPage - 1) * pagination.itemsPerPage + 1;
  const lastResultNumber = Math.min(firstResultNumber + pagination.itemsPerPage, pagination.totalItems);
  return (
    <div className="d-flex justify-content-between">
      <div className="d-flex align-items-center justify-content-center">
        <span>
          Results {firstResultNumber} - {lastResultNumber} displayed of {pagination.totalItems}
        </span>
        <div className="d-flex align-items-center ml-1">
          <span>{'(Maximum results per page'}</span>
          <span className="dropdown p-2">
            <button
              className="btn btn-secondary dropdown-toggle p-2"
              type="button"
              id="dropdownMenuButton"
              data-toggle="dropdown"
            >
              {pagination.itemsPerPage}
            </button>
            <div className="dropdown-menu" style={{ minWidth: '5rem' }}>
              {perPageOptions.map((option) => (
                <div key={option} className="dropdown-item p-0" onClick={() => onPerPageSelection(option)}>
                  <button className="btn btn-light p-1">{option}</button>
                </div>
              ))}
            </div>
          </span>
          {')'}
        </div>
      </div>
      <div>
        <div className="dropdown d-flex p-2">
          <span className="text-nowrap m-2">Sort By:</span>
          <button
            className="btn btn-outline-secondary dropdown-toggle p-2"
            type="button"
            id="dropdownSortButton"
            data-toggle="dropdown"
          >
            {sortKeyOptions[activeSortKey].label}
          </button>
          <div className="dropdown-menu dropdown-menu-right" style={{ minWidth: '10rem' }}>
            {Object.entries(sortKeyOptions).map(([key, value]) => (
              <div className="dropdown-item p-0" key={key}>
                <button className="btn btn-light p-1" onClick={() => onSortKeySelection(key)}>
                  {value.label}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
