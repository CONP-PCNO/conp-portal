import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import DataTable from "./DataTable";

const DataTableContainer = ({
  endpointURL,
  limit,
  authorized,
  total,
  sortKeys,
  elements,
  ...dataTableProps
}) => {
  const [fetchedElements, setFetchedElements] = React.useState(elements);

  const [query, setQuery] = React.useState({
    search: "",
    sortKey: "title",
    sortComparitor: "asc",
    cursor: 0,
    limit
  });

  const [totalState, setTotalState] = React.useState(total);

  const [sortKeysState, setSortKeysState] = React.useState(sortKeys);
  const [authorizedState, setAuthorizedState] = React.useState(authorized);

  React.useEffect(() => {
    setQuery({ ...query, limit });
  }, [limit]);

  const fetchElements = async () => {
    const url = `${endpointURL}?${qs.stringify(query)}`;

    console.log(`Fetching from: ${url}`);

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
      total={totalState}
      sortKeys={sortKeysState}
      query={query}
      setQuery={setQuery}
      {...dataTableProps}
    />
  );
};

DataTableContainer.propTypes = {
  authorized: PropTypes.bool,
  endpointURL: PropTypes.string,
  limit: PropTypes.number,
  total: PropTypes.number,
  elements: PropTypes.arrayOf(PropTypes.object)
};

DataTableContainer.defaultProps = {
  authorized: false,
  endpointURL: "",
  limit: 10,
  total: 0,
  elements: []
};

export default DataTableContainer;
