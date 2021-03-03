import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import * as qs from "query-string";

import DataTable from "./DataTable";

const DataTableContainer = ({
  endpointURL,
  imagePath,
  limit,
  authorized,
  total,
  page,
  max_per_page,
  elements,
  filters,
  ...dataTableProps
}) => {
  const [fetchedElements, setFetchedElements] = useState(elements);

  const [query, setQuery] = useState({
    search: filters.search ? filters.search : "",
    modalities: filters.modalities ? filters.modalities : [],
    formats: filters.formats ? filters.formats : [],
    sortKey: filters.sortKey ? filters.sortKey : "conpStatus",
    sortComparitor: filters.sortComparitor ? filters.sortComparitor : "asc",
    page: filters.page ? filters.page : 1,
    max_per_page: filters.max_per_page ? filters.max_per_page : 10,
    cursor: filters.cursor ? filters.cursor : 0,
    limit: filters.limit ? filters.limit : 10
  });

  const [totalState, setTotalState] = useState(total);

  const [sortKeysState, setSortKeysState] = useState();
  const [filterKeysState, setFilterKeysState] = useState();
  const [authorizedState, setAuthorizedState] = useState(authorized);

  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setQuery({ ...query, limit });
  }, [limit]);

  useEffect(() => {
    // Remove empty keys from query and set query object as query parameters
    // Repeat this every time the query changes to ensure query state survives refresh / back navigation
    const q = query
    Object.keys(q).forEach(k => {
      if (q[k] === '' || (Array.isArray(q[k]) && q[k].length === 0)) {
        delete q[k]
      }
    })
    const queryString = new URLSearchParams(q).toString()
    const pathname = window.location.pathname
    window.history.replaceState(null, null, `${pathname}?${queryString}`)
  }, [query])

  const fetchElements = async () => {
    const url = `${endpointURL}?${qs.stringify(query, { arrayFormat: 'comma' })}`;

    try {
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(
          `Request failed with status: ${res.status} (${res.statusText})`
        );
      }

      const parsed = await res.json();

      setFetchedElements(parsed.elements);
      setTotalState(parsed.total);
      setSortKeysState(parsed.sortKeys);
      setFilterKeysState(parsed.filterKeys);
      setAuthorizedState(parsed.authorized);
    }
    catch (err) {
      alert("There was an error retrieving the search results.");
      console.error(err);
    }
    finally {
      isLoading && setIsLoading(false)
      setTimeout(() => {
        window.scrollTo(0, 0)
      }, 100)
    }
  };

  useEffect(() => {
    fetchElements()
  }, [query])

  return (
    <DataTable
      authorized={authorizedState}
      elements={fetchedElements}
      imagePath={imagePath}
      total={totalState}
      sortKeys={sortKeysState}
      filterKeys={filterKeysState}
      query={query}
      setQuery={setQuery}
      isLoading={isLoading}
      {...dataTableProps}
    />
  );
};

DataTableContainer.propTypes = {
  authorized: PropTypes.bool,
  endpointURL: PropTypes.string.isRequired,
  imagePath: PropTypes.string,
  limit: PropTypes.number,
  total: PropTypes.number,
  page: PropTypes.number,
  max_per_page: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number
  ]),
  elements: PropTypes.arrayOf(PropTypes.object),
};

DataTableContainer.defaultProps = {
  authorized: false,
  endpointURL: "",
  imagePath: 'static/img/',
  limit: 10,
  total: 0,
  page: 1,
  max_per_page: 10,
  elements: [],
  modalities: [],
  formats: []
};

export default DataTableContainer;
