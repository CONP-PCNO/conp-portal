import * as R from "ramda";
import React from "react";
import PropTypes from "prop-types";

const DataTable = ({
  authorized,
  sortKeys,
  elements,
  total,
  renderElement,
  query,
  setQuery
}) => {
  return (
    <div className="search-dataset-table container" cellSpacing={0}>
      <div className="searchbar col-12 d-flex p-2">
        <div className="d-flex dropdown">
          <label className="dropdown-label m-2">Sort By: </label>
          <select
            className="btn btn-outline-secondary dropdown-toggle dropdown-select px-4"
            value={query.sortKey}
            onChange={e =>
              setQuery({ ...query, sortKey: e.currentTarget.value })
            }
          >
            {sortKeys.map(({ key: sortKey, label }, i) => (
              <option className="dropdown-item" key={i} value={sortKey}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <div className="input-group pt-2 pt-md-0">
          <input
            className="form-control"
            type="text"
            placeholder="Search"
            aria-label="Search"
            value={query.search}
            onChange={e =>
              setQuery({ ...query, search: e.currentTarget.value })
            }
          />
          <span className="input-group-append">
            <span className="input-group-text" id="basic-addon2">
              <i className="fa fa-search" />
            </span>
          </span>
        </div>
      </div>
      {elements.map((element, i) => (
        <div key={element.id} className="container">
          {React.createElement(renderElement, { ...element, authorized })}
        </div>
      ))}
      <div className="search-dataset-footer d-flex align-items-center p-2">
        <div className="btn-group">
          <div className="btn btn-outline-dark btn-sm"
            onClick={e =>
              setQuery({ ...query, page: 1 })
            }>&lt;&lt;</div>
          <div className="btn btn-outline-dark btn-sm"
           onClick={e =>
            setQuery({ ...query, page: Math.max(1, query.page-1) })
          }> &lt; </div>
          {R.range(1, Math.ceil(total / query.max_per_page)).map(
            (page, i) => (
              <div className={page === query.page ? "btn btn-dark btn-sm" : "btn btn-outline-dark btn-sm"}
              onClick={e =>
                setQuery({ ...query, page: page })
              }
                key={i}>
                {page}
              </div>
            )
          )}
          <div className="btn btn-outline-dark btn-sm"
            onClick={e =>
              setQuery({ ...query, page: Math.min(query.page+1, Math.ceil(total / query.max_per_page)) })
            }
          >
            &gt;
          </div>
          <div className="btn btn-outline-dark btn-sm"
            onClick={e =>
              setQuery({ ...query, page: Math.ceil(total / query.max_per_page) })
            }
          >
            &gt;&gt;
          </div>
        </div>
      </div>
    </div>
  );
};


DataTable.propTypes = {
  authorized: PropTypes.bool,
  sortKeys: PropTypes.arrayOf(
    PropTypes.shape({ key: PropTypes.string, label: PropTypes.string })
  ),
  elements: PropTypes.arrayOf(PropTypes.object),
  total: PropTypes.number,
  renderElement: PropTypes.func,
  query: PropTypes.shape({
    search: PropTypes.string,
    sortKey: PropTypes.string,
    page: PropTypes.number,
    max_per_page: PropTypes.number,
    sortComparitor: PropTypes.string,
    cursor: PropTypes.number,
    limit: PropTypes.number
  }),
  setQuery: PropTypes.func
};

DataTable.defaultProps = {
  sortKeys: [],
  elements: [],
  total: 0
};

export default DataTable;
