import React, { useContext } from 'react';

import { ExperimentTableContext } from '../../context/ExperimentTableContext';

export const PaginationNav = () => {
  const { pagination, setCurrentPage } = useContext(ExperimentTableContext)!;

  const lastPage = Math.ceil(pagination.totalItems / pagination.itemsPerPage) - 1;
  const pageIndices = [...Array(lastPage + 1).keys()];

  const handlePageChange = (newPageIndex: number) => {
    if (newPageIndex >= 0 && newPageIndex <= lastPage) {
      setCurrentPage(newPageIndex);
    }
  };

  return (
    <div className="search-dataset-footer d-flex align-items-center p-2">
      <div className="btn-group">
        <button className="btn btn-outline-dark" onClick={() => setCurrentPage(0)}>
          &lt;&lt;
        </button>
        <button className="btn btn-outline-dark" onClick={() => handlePageChange(pagination.currentPage - 1)}>
          &lt;
        </button>
        {pageIndices.map((i) => (
          <button
            className={`btn ${i === pagination.currentPage ? 'btn-dark' : 'btn-outline-dark'}`}
            key={i}
            onClick={() => handlePageChange(i)}
          >
            {i + 1}
          </button>
        ))}
        <button className="btn btn-outline-dark" onClick={() => handlePageChange(pagination.currentPage + 1)}>
          &gt;
        </button>
        <button className="btn btn-outline-dark" onClick={() => setCurrentPage(lastPage)}>
          &gt;&gt;
        </button>
      </div>
    </div>
  );
};
