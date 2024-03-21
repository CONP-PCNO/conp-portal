import * as R from "ramda";
import React, { useState } from "react";
import PropTypes from "prop-types";

const DataTable = ({
  authorized,
  sortKeys,
  filterKeys,
  elements,
  imagePath,
  total,
  renderElement,
  cbrainIds,
  query,
  setQuery,
  isLoading
}) => {
  const [filters, setFilters] = useState([
    {
      key: "modalities",
      values: query.modalities || []
    },
    {
      key: "formats",
      values: query.formats || []
    },
    {
      key: "cbrain",
      values: query.cbrain || []
    },
    {
      key: "authorizations",
      values: query.authorizations || []
    }
  ]);

  const [tempSearch, setTempSearch] = useState(query.search)
  // const handleFiltersChange = (event) => {
  //   event.preventDefault();
  //   const e = event.target.value;
  //   const filter = e.split(".");
  //   const newFilters = filters;
  //   newFilters.forEach(f => {
  //     if (f.key === filter[0]) {
  //       if (f.values.includes(filter[1])) {
  //         f.values.splice(f.values.indexOf(filter[1]), 1);
  //       } else {
  //         f.values.push(filter[1])
  //       }
  //     }
  //   })
  //   setFilters(newFilters);
  //   setQuery({
  //     ...query,
  //     modalities: filters.filter(f => f["key"] === "modalities")[0].values,
  //     formats: filters.filter(f => f["key"] === "formats")[0].values,
  //     cbrain: filters.filter(f => f["key"] === "cbrain")[0].values,
  //     authorizations: filters.filter(f => f["key"] === "authorizations")[0].values,
  //     page: 1
  //   })
  // }

  const handleFiltersChange = (event) => {
    event.preventDefault();
    const e = event.target.value;
    const [filterKey, filterValue] = e.split(".");

    // Créer une copie profonde des filtres pour éviter les mutations directes
    const newFilters = filters.map(f => ({
      ...f,
      values: f.key === filterKey ? 
        f.values.includes(filterValue) ? 
          f.values.filter(value => value !== filterValue) // Retirer la valeur si elle existe déjà
          : [...f.values, filterValue] // Ajouter la valeur si elle n'existe pas
        : [...f.values]
    }));

    setFilters(newFilters);

    // Mise à jour de `query` basée sur les nouveaux filtres
    const updatedQuery = {
      ...query,
      modalities: newFilters.find(f => f.key === "modalities")?.values || [],
      formats: newFilters.find(f => f.key === "formats")?.values || [],
      cbrain: newFilters.find(f => f.key === "cbrain")?.values || [],
      authorizations: newFilters.find(f => f.key === "authorizations")?.values || [],
      page: 1 // Réinitialiser à la première page à chaque modification de filtre
    };

    setQuery(updatedQuery);
  };


  const handleMaxPerPageChange = (event) => {
    event.preventDefault()
    const value = event.target.value;
    setQuery({
      ...query,
      max_per_page: value,
      limit: value,
      page: 1
    })
  }

  const handlePageChange = (event) => {
    event.preventDefault()
    let page;
    const value = event.target.value;
    switch (value) {
      case 'first':
        page = 1;
        break;
      case 'back':
        page = Math.max(1, query.page - 1);
        break
      case 'forward':
        page = Math.min(query.page + 1, Math.ceil(total / query.max_per_page));
        break;
      case 'last':
        page = Math.ceil(total / query.max_per_page);
        break;
      default:
        page = parseInt(value);
    }
    setQuery({ ...query, page: page })
  }

   // Fonction pour filtrer les éléments basée sur les filtres actifs
   const filterElements = (elements, filters) => {
    return elements.filter(element => {
      return filters.every(filter => {
        if (filter.values.length === 0) {
          return true; // Si aucun filtre n'est actif pour cette clé, l'élément passe
        }
        const elementValue = element[filter.key];
        if (Array.isArray(elementValue)) {
          return filter.values.some(value => elementValue.includes(value));
        } else {
          return filter.values.includes(elementValue);
        }
      });
    });
  };

  const filteredElements = filterElements(elements, filters);

  return (
    isLoading ? <div />
      :
        < div className="search-dataset-table" cellSpacing={0}>
          <div className="searchbar d-flex flex-column">
            <div className="d-flex align-items-center">
              {renderElement.name === "DatasetElement" ?
                  <div className="d-flex align-items-center p-2">
                    <label className="dropdown-label text-nowrap m-2">Filter By: </label>
                    <div className="dropdown">
                      <button className="btn btn-outline-secondary dropdown-toggle p-2" type="button"
                              id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                              data-display="static">
                        Modality:
                      </button>
                      <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        {filterKeys.filter(f => f["key"] === "modalities").length > 0 ?
                            filterKeys.filter(f => f["key"] === "modalities")[0]["values"].map(modality => (
                                modality !== '' ?
                                    <div key={modality.id} className="dropdown-item ml-2">
                                      <input className="form-check-input" type="checkbox"
                                             checked={filters.filter(f => f["key"] === "modalities")[0]["values"].includes(modality)}
                                             value={"modalities." + modality} id={"filter" + modality}
                                             onChange={handleFiltersChange}/>
                                      <label className="form-check-label" htmlFor={"filter" + modality}>
                                        {modality}
                                      </label>
                                    </div>
                                    : null
                            ))
                            : null}
                      </div>
                    </div>
                    <div className="dropdown">
                      <button className="btn btn-outline-secondary dropdown-toggle p-2" type="button"
                              id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                              data-display="static">
                        File Format:
                      </button>
                      <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        {filterKeys.filter(f => f["key"] === "formats").length > 0 ?
                            filterKeys.filter(f => f["key"] === "formats")[0]["values"].map(format => (
                                format !== '' ?
                                    <div key={format.id} className="dropdown-item ml-2">
                                      <input className="form-check-input" type="checkbox"
                                             checked={filters.filter(f => f["key"] === "formats")[0]["values"].includes(format)}
                                             value={"formats." + format} id={"filter" + format}
                                             onChange={handleFiltersChange}/>
                                      <label className="form-check-label" htmlFor={"filter" + format}>
                                        {format}
                                      </label>
                                    </div>
                                    : null
                            ))
                            : null}
                      </div>
                    </div>
                    <div className="dropdown">
                      <button className="btn btn-outline-secondary dropdown-toggle p-2" type="button"
                              id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"
                              data-display="static">
                        Third-party account required:
                      </button>
                      <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        {filterKeys.filter(f => f["key"] === "authorizations").length > 0 ?
                            filterKeys.filter(f => f["key"] === "authorizations")[0]["values"].map(authorizations => (
                                authorizations !== '' ?
                                    <div key={authorizations.id} className="dropdown-item ml-2">
                                      <input className="form-check-input" type="checkbox"
                                             checked={filters.filter(f => f["key"] === "authorizations")[0]["values"].includes(authorizations)}
                                             value={"authorizations." + authorizations} id={"filter" + authorizations}
                                             onChange={handleFiltersChange}/>
                                      <label className="form-check-label" htmlFor={"filter" + authorizations}>
                                        {authorizations}
                                      </label>
                                    </div>
                                    : null
                            ))
                            : null}
                      </div>
                    </div>
                  </div>
                  : null}

              {renderElement.name === "PipelineElement" || renderElement.name === "DatasetElement" ?
	          <form className="input-group m-2" onSubmit={e => {setQuery({...query, search: tempSearch, page: 1}); e.preventDefault();}}>
                    <input
                        className="form-control p-2"
                        type="text"
                        placeholder="Search"
                        aria-label="Search"
		        id="searchInput"
                        value={tempSearch}
                        onChange={e =>
                            setTempSearch(e.currentTarget.value)
                        }
                    />
                    <span className="input-group-append">
                      <button className="input-group-text" id="basic-addon2">
                        <i className="fa fa-search"/>
                      </button>
                    </span>
	          </form>
                  : null}
              {renderElement.name === "ExecutionRecordElement" ?
                  <div className="input-group m-2">
                    <input
                        className="form-control p-2"
                        id="Search for Pipeline"
                        type="text"
                        placeholder="Search for pipeline"
                        aria-label="Search for pipeline"
                        value={query.searchPipelineName}
                        onChange={e =>
                            setQuery({...query, searchPipelineName: e.currentTarget.value, page: 1})
                        }
                    />
                    <span className="input-group-append pr-2">
                  <span className="input-group-text" id="basic-addon2">
                    <i className="fa fa-search"/>
                  </span>
                </span>

                    <input
                        className="form-control p-2"
                        id="Search for Dataset"
                        type="text"
                        placeholder="Search for dataset"
                        aria-label="Search for dataset"
                        value={query.searchDatasetName}
                        onChange={e =>
                            setQuery({...query, searchDatasetName: e.currentTarget.value, page: 1})
                        }
                    />
                    <span className="input-group-append ">
                  <span className="input-group-text" id="basic-addon2">
                    <i className="fa fa-search"/>
                  </span>
                </span>
                  </div>
                  : null
              }

            </div>
            <div className="d-flex justify-content-between">
              <div className="d-flex justify-content-start align-items-center pb-1 pl-3 ml-4">
                      <div key={"cbrain".id}>
                        <input className="form-check-input" type="checkbox" id="filterCBRAIN"
                               checked={filters.filter(f => f["key"] === "cbrain")[0].values.includes("cbrain_id")}
                               value="cbrain.cbrain_id"
                               onChange={handleFiltersChange}/>
                        <label className="form-check-label" htmlFor="filterCBRAIN">
                          Available in CBRAIN
                        </label>
                      </div>
              </div>


              {renderElement.name === "PipelineElement" ?
                <div className="d-flex justify-content-end align-items-center pb-1 pr-3">
                  <a className="text-reset px-1" href="/execution-records">
                    Browse pipeline execution records
                  </a>
                </div>
                : null}

              {renderElement.name === "DatasetElement" ?
                <div className="d-flex justify-content-end align-items-center pb-1 pr-3">
                  <a className="text-reset px-1" href="/sparql">
                    Advanced Search Page (NEXUS)
                  </a>
                </div>
                : null}
            </div>
          </div>

          <div className="d-flex justify-content-between">
            <div className="d-flex p-2 justify-content-start align-items-center">
              {query.max_per_page === 'All' ?
                  `Displaying ${total} results.` :
                  `Results ${(query.max_per_page * (query.page - 1)) + 1} - ${Math.min((query.max_per_page * query.page), total)} displayed of ${total}.`} (Maximum
              results per page
              <span className="dropdown p-2">
              <button className="btn btn-secondary dropdown-toggle p-2" type="button" id="dropdownMenuButton"
                      data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                {query.max_per_page}
              </button>
              <div className="dropdown-menu" style={{minWidth: '5rem'}}>
                <div key="max_per_page_5" className="dropdown-item p-0">
                  <button type="button" className="btn btn-light p-1" value={5} id={"max_per_page." + 5}
                          onClick={handleMaxPerPageChange}>
                    5
                    </button>
                </div>
                <div key="max_per_page_10" className="dropdown-item p-0">
                  <button type="button" className="btn btn-light p-1" value={10} id={"max_per_page." + 10}
                          onClick={handleMaxPerPageChange}>
                    10
                    </button>
                </div>
                <div key="max_per_page_15" className="dropdown-item p-0">
                  <button type="button" className="btn btn-light p-1" value={15} id={"max_per_page." + 15}
                          onClick={handleMaxPerPageChange}>
                    15
                    </button>
                </div>
                <div key="max_per_page_20" className="dropdown-item p-0">
                  <button type="button" className="btn btn-light p-1" value={20} id={"max_per_page." + 20}
                          onClick={handleMaxPerPageChange}>
                    20
                    </button>
                </div>
                <div key="max_per_page_all" className="dropdown-item p-0">
                  <button type="button" className="btn btn-light p-1" value={"All"} id={"max_per_page.all"}
                          onClick={handleMaxPerPageChange}>
                    All
                    </button>
                </div>
              </div>
            </span>)
            </div>

            {renderElement.name === "PipelineElement" || renderElement.name === "DatasetElement" ?

                <div className="d-flex align-items-center dropdown p-2">
                  <label className="dropdown-label text-nowrap m-2">Sort By: </label>
                  <select
                      className="btn btn-outline-secondary dropdown-toggle dropdown-select p-2"
                      value={query.sortKey}
                      onChange={e =>
                          setQuery({...query, sortKey: e.currentTarget.value, page: 1})
                      }
                  >
                    {sortKeys.map(({key: sortKey, label}, i) => (
                        <option className="dropdown-item" key={i} value={sortKey}>
                          {label}
                        </option>
                    ))}
                  </select>
                </div>
                : null}

          </div>

          {renderElement.name === "ExecutionRecordElement" ?
              <div className="card flex-row" data-type="pipeline">
                <div className="d-flex col-md-12">
                  <div className="d-flex py-1 w-100">
                    <div className="col-5">
                <span>
                  <a>Pipeline Name</a>
                </span>
                    </div>
                    <div className="col-5">
                <span>
                  <a>Dataset Name</a>
                </span>
                    </div>
                    <div className="col-2">
                <span>
                  <a>Execution Result</a>
                </span>
                    </div>
                  </div>
                </div>
              </div>
              : null}
          {
            filteredElements.map((element, i) => {
              return (
                <div key={"" + element.id}>
                  {React.createElement(renderElement, {...element, authorized, imagePath, cbrainIds})}
                </div>
              );
            })
          }
          {
            query.max_per_page !== 'All' ?
                <div className="search-dataset-footer d-flex align-items-center p-2">
                  <div className="btn-group">
                    <button className="btn btn-outline-dark" value="first"
                            onClick={handlePageChange}>
                      &lt;&lt;
                    </button>
                    <button className="btn btn-outline-dark" value="back"
                            onClick={handlePageChange}> &lt; </button>
                    {R.range(1, Math.ceil(total / query.max_per_page) + 1).map(
                        (page, i) => {
                          {
                            return ((page < (10 + query.page)) && (page >= query.page)) ?
                                <button className={page === query.page ? "btn btn-dark" : "btn btn-outline-dark"}
                                        value={page}
                                        onClick={handlePageChange}
                                        key={i}>
                                  {page}
                                </button> : null
                          }
                        }
                    )}
                    <button className="btn btn-outline-dark" value="forward"
                            onClick={handlePageChange}
                    >
                      &gt;
                    </button>
                    <button className="btn btn-outline-dark" value="last"
                            onClick={handlePageChange}
                    >
                      &gt;&gt;
                    </button>
                  </div>
                </div>
                : null
          }
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
  cbrainIds: PropTypes.arrayOf(PropTypes.string),
  query: PropTypes.shape({
    search: PropTypes.string,
    searchPipelineName: PropTypes.string,
    searchDatasetName: PropTypes.string,
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
    },
    {
      key: "cbrain",
      values: []
    },
    {
      key: "authorizations",
      values: []
    }
  ],
  elements: [],
  total: 0,
  imagePath: 'static/img/'
};

export default DataTable;
