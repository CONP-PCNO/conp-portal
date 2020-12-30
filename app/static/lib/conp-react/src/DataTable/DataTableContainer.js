import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
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
  const [fetchedElements, setFetchedElements] = React.useState(elements);

  const [query, setQuery] = React.useState({
    search: filters.search ? filters.search : "",
    tags: filters.tags ? filters.tags.split(",") : [],
    modalities: filters.modalities ? filters.modalities.split(",") : [],
    formats: filters.formats ? filters.formats.split(",") : [],
    sortKey: "conpStatus",
    sortComparitor: "asc",
    page,
    max_per_page,
    cursor: 0,
    limit
  });

  const [totalState, setTotalState] = React.useState(total);

  const [sortKeysState, setSortKeysState] = React.useState();
  const [filterKeysState, setFilterKeysState] = React.useState();
  const [authorizedState, setAuthorizedState] = React.useState(authorized);

  React.useEffect(() => {
    setQuery({ ...query, limit });
  }, [limit]);

  React.useEffect(() => {
    // Remove empty keys from query and set query object as query parameters
    // Repeat this every time the query changes to ensure query state survives refresh / back navigation
    const q = query
    Object.keys(q).forEach(k => {
      if (q[k] === '' || (Array.isArray(q[k]) && q[k].length === 0)) {
        delete q[k]
      }
    })
    const queryString = new URLSearchParams(q).toString()
    window.history.replaceState(null, null, `/search?${queryString}`)
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
    } catch (err) {
      alert("There was an error retrieving the search results.");
      console.error(err);
    }
  };

  useDebounce(() => void fetchElements(), 300, [endpointURL, query]);

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
