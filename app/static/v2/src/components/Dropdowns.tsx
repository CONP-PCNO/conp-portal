import React from 'react';

export interface SortKeyOptions {
  [key: string]: {
    column: string;
    label: string;
  };
}

export interface Pagination {
  page: number;
  perPage: number;
  total: number;
}

export interface DropdownsProps {
  activeSortKey: string;
  sortKeyOptions: SortKeyOptions;
  pagination: Pagination;
  perPageOptions?: number[];
}

export const Dropdowns = ({
  activeSortKey,
  sortKeyOptions,
  pagination,
  perPageOptions = [5, 10, 15, 20]
}: DropdownsProps) => {
  const firstResultNumber = (pagination.page - 1) * pagination.perPage + 1;
  const lastResultNumber = Math.min(firstResultNumber + pagination.perPage, pagination.total);
  return (
    <div className="d-flex justify-content-between">
      <div>
        <span>
          Results {firstResultNumber} - {lastResultNumber} displayed of {pagination.total}
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
              {pagination.perPage}
            </button>
            <div className="dropdown-menu" style={{ minWidth: '5rem' }}>
              {perPageOptions.map((option) => (
                <div
                  key={option}
                  className="dropdown-item p-0"
                  onClick={() => console.log("experiments.updateSearchParam('per_page', '{{ option }}')")}
                >
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
            {activeSortKey ?? 'Active Sort Key'}
          </button>
          <div className="dropdown-menu dropdown-menu-right" style={{ minWidth: '10rem' }}>
            {Object.entries(sortKeyOptions).map(([key, value]) => (
              <div className="dropdown-item p-0" key={key}>
                <button
                  className="btn btn-light p-1"
                  onClick={() => console.log("experiments.updateSearchParam('sort_key', '{{ option }}')")}
                >
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
