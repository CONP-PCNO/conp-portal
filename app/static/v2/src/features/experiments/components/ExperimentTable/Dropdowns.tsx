import React from 'react';

import { useExperimentTableStore } from '@/features/experiments/store/experiment-table-store';

const perPageOptions = [5, 10, 15, 20];

export const Dropdowns = () => {
  const store = useExperimentTableStore();

  const firstResultNumber = (store.pagination.currentPage - 1) * store.pagination.itemsPerPage + 1;
  const lastResultNumber = Math.min(firstResultNumber + store.pagination.itemsPerPage, store.items.length);
  return (
    <div className="d-flex justify-content-between">
      <div className="d-flex align-items-center justify-content-center">
        <span>
          Results {firstResultNumber} - {lastResultNumber} displayed of {store.items.length}
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
              {store.pagination.itemsPerPage}
            </button>
            <div className="dropdown-menu" style={{ minWidth: '5rem' }}>
              {perPageOptions.map((option) => (
                <div key={option} className="dropdown-item p-0" onClick={() => store.setItemsPerPage(option)}>
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
            {store.sortKey.options[store.sortKey.active].label}
          </button>
          <div className="dropdown-menu dropdown-menu-right" style={{ minWidth: '10rem' }}>
            {Object.entries(store.sortKey.options).map(([key, value]) => (
              <div className="dropdown-item p-0" key={key}>
                <button className="btn btn-light p-1" onClick={() => store.setActiveSortKey(key)}>
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
