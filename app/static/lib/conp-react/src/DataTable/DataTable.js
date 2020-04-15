import * as R from "ramda";
import React, { useState } from "react";
import PropTypes from "prop-types";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUserLock } from '@fortawesome/free-solid-svg-icons'
import { faUserAlt } from '@fortawesome/free-solid-svg-icons'

const DataTable = ({
  authorized,
  sortKeys,
  filterKeys,
  elements,
  imagePath,
  total,
  renderElement,
  query,
  setQuery
}) => {
  const [filters, setFilters] = useState([
    {
      key: "modalities",
      values: []
    },
    {
      key: "formats",
      values: []
    }
  ]);

  const handleChange = (event) => {
    const e = event.target.value;
    const filter = e.split(".");
    const newFilters = filters;
    newFilters.map(f => {
      if (f.key === filter[0]){
        if(f.values.includes(filter[1])){
          f.values.splice(f.values.indexOf(filter[1]), 1);
        }
        else {
          f.values.push(filter[1])
        }
      }
    })
    setFilters(newFilters);
    setQuery({
      ...query,
      modalities: filters.filter(f => f["key"] == "modalities")[0].values,
      formats: filters.filter(f => f["key"] == "formats")[0].values,
      page: 1
    })
  }

  return (
    <div className="search-dataset-table container" cellSpacing={0}>
      <div className="searchbar col-12 d-flex p-2">
        <div className="d-flex dropdown">
          <label className="dropdown-label m-2">Sort By: </label>
          <select
            className="btn btn-outline-secondary dropdown-toggle dropdown-select"
            value={query.sortKey}
            onChange={e =>
              setQuery({ ...query, sortKey: e.currentTarget.value, page: 1 })
            }
          >
            {sortKeys.map(({ key: sortKey, label }, i) => (
              <option className="dropdown-item" key={i} value={sortKey}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <div className="input-group m-2">
          <input
            className="form-control p-2"
            type="text"
            placeholder="Search"
            aria-label="Search"
            value={query.search}
            onChange={e =>
              setQuery({ ...query, search: e.currentTarget.value, page: 1 })
            }
          />
          <span className="input-group-append">
            <span className="input-group-text" id="basic-addon2">
              <i className="fa fa-search" />
            </span>
          </span>
        </div>
      </div>
      {renderElement.name == "DatasetElement" ?
        <div className="d-flex justify-content-between">
          <div className="d-flex p-2 justify-content-start align-items-center">
            <div className="p-1 text-nowrap text-truncate"><FontAwesomeIcon icon={faUserAlt} color="dimgray" size="lg" />: CONP account required</div>
            <div className="p-1 text-nowrap text-truncate"><FontAwesomeIcon icon={faUserLock} color="dimgray" size="lg" />: Third-party account required</div>
          </div>
          <div className="d-flex p-2 justify-content-end">
            <div className="dropdown">
              <button className="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Modality:
          </button>
              <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                {filterKeys.filter(f => f["key"] == "modalities").length > 0 ?
                filterKeys.filter(f => f["key"] == "modalities")[0]["values"].map(modality => (
                  <div key={modality.id} className="dropdown-item ml-2">
                    <input className="form-check-input" type="checkbox" value={"modalities." + modality} id={"filter" + modality} onChange={handleChange} />
                    <label className="form-check-label" htmlFor={"filter" + modality}>
                      {modality}
                    </label>
                  </div>
                )): null}
              </div>
            </div>
            <div className="dropdown">
              <button className="btn btn-light dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                File Format:
          </button>
              <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                {filterKeys.filter(f => f["key"] == "formats").length > 0 ?
                filterKeys.filter(f => f["key"] == "formats")[0]["values"].map(format => (
                  <div key={format.id} className="dropdown-item ml-2">
                    <input className="form-check-input" type="checkbox" value={"formats." + format} id={"filter" + format} onChange={handleChange} />
                    <label className="form-check-label" htmlFor={"filter" + format}>
                      {format}
                    </label>
                  </div>
                )): null}
              </div>
            </div>
          </div>
        </div> : null}
      {elements.map((element, i) => (
        <div key={"" + element.id} className="container">
          {React.createElement(renderElement, { ...element, authorized, imagePath })}
        </div>
      ))}
      <div className="search-dataset-footer d-flex align-items-center p-2">
        <div className="btn-group">
          <div className="btn btn-outline-dark"
            onClick={e =>
              setQuery({ ...query, page: 1 })
            }>&lt;&lt;</div>
          <div className="btn btn-outline-dark"
            onClick={e =>
              setQuery({ ...query, page: Math.max(1, query.page - 1) })
            }> &lt; </div>
          {R.range(1, Math.ceil(total / query.max_per_page) + 1).map(
            (page, i) => (
              <div className={page === query.page ? "btn btn-dark" : "btn btn-outline-dark"}
                onClick={e =>
                  setQuery({ ...query, page: page })
                }
                key={i}>
                {page}
              </div>
            )
          )}
          <div className="btn btn-outline-dark"
            onClick={e =>
              setQuery({ ...query, page: Math.min(query.page + 1, Math.ceil(total / query.max_per_page)) })
            }
          >
            &gt;
          </div>
          <div className="btn btn-outline-dark"
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
  imagePath: PropTypes.string,
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
  filterKeys: [
    {
      key: "modalities",
      values: []
    },
    {
      key: "formats",
      values: []
    }
  ],
  elements: [],
  total: 0,
  imagePath: 'static/img/'
};

export default DataTable;
