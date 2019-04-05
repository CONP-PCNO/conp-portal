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
    <div className="search-dataset-table" cellSpacing={0}>
      <div className="search-dataset-toolbar">
        <div className="input-group">
          <label className="input-group-addon">Sort By:</label>
          <select
            className="form-control"
            value={query.sortKey}
            onChange={e =>
              setQuery({ ...query, sortKey: e.currentTarget.value })
            }
          >
            {sortKeys.map(({ key: sortKey, label }, i) => (
              <option key={i} value={sortKey}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <div className="input-group">
          <input
            className="form-control"
            style={{ width: "350px" }}
            value={query.search}
            onChange={e =>
              setQuery({ ...query, search: e.currentTarget.value })
            }
          />
          <span className="input-group-addon">
            <i className="fa fa-search" />
          </span>
        </div>
      </div>
      {elements.map((element, i) => (
        <div
          key={i}
          style={{
            borderBottom: "solid",
            borderBottomWidth: i === elements.length - 1 ? "0px" : "1px"
          }}
        >
          {React.createElement(renderElement, element)}
        </div>
      ))}
      <div className="search-dataset-footer">
        <ul className="pagination">
          <li
            onClick={() =>
              setQuery({
                ...query,
                cursor: Math.max(query.cursor - query.limit, 0)
              })
            }
          >
            <a href="#">&laquo;</a>
          </li>
          {R.range(1, Math.max(Math.floor(total / query.limit) + 1, 2)).map(
            (page, i) => (
              <li
                key={i}
                onClick={() =>
                  setQuery({ ...query, cursor: (page - 1) * query.limit })
                }
                className={
                  page === Math.floor(query.cursor / query.limit) + 1
                    ? "active"
                    : ""
                }
              >
                <a href="#">{page}</a>
              </li>
            )
          )}
          <li
            onClick={() =>
              setQuery({
                ...query,
                cursor: Math.max(
                  Math.min(query.cursor + query.limit, total - query.limit),
                  0
                )
              })
            }
          >
            <a href="#">&raquo;</a>
          </li>
        </ul>
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
