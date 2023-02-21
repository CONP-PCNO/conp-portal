import React, { useContext } from 'react';

import { ExperimentTableContext } from '../../context/ExperimentTableContext';

const perPageOptions = [5, 10, 15, 20];

export const Dropdowns = () => {
  const { setItemsPerPage, setActiveSortKey, sortKey, pagination } = useContext(ExperimentTableContext)!;
  return (
    <div className="d-flex justify-content-between">
      <div className="d-flex align-items-center justify-content-center">
        <span>
          Results {pagination.firstItemIndex + 1} - {pagination.lastItemIndex + 1} displayed of {pagination.totalItems}
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
                <div key={option} className="dropdown-item p-0" onClick={() => setItemsPerPage(option)}>
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
            {sortKey.options[sortKey.active].label}
          </button>
          <div className="dropdown-menu dropdown-menu-right" style={{ minWidth: '10rem' }}>
            {Object.entries(sortKey.options).map(([key, value]) => (
              <div className="dropdown-item p-0" key={key}>
                <button className="btn btn-light p-1" onClick={() => setActiveSortKey(key)}>
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
