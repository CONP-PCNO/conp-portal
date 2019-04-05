import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import DataTable from "./DataTable";
import AppContext from "../AppContext";

const DataTableContainer = ({
  authorized,
  endpointURL,
  limit,
  total,
  imagePath,
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
    } catch (err) {
      alert("There was an error retrieving the search results.");
      console.error(err);
    }
  };

  useDebounce(() => void fetchElements(), 1000, [endpointURL, query]);

  return (
    <AppContext.Provider value={{ imagePath }}>
      <DataTable
        authorized={authorized}
        elements={fetchedElements}
        total={totalState}
        query={query}
        setQuery={setQuery}
        {...dataTableProps}
      />
    </AppContext.Provider>
  );
};

DataTableContainer.propTypes = {
  authorized: PropTypes.bool,
  endpointURL: PropTypes.string,
  limit: PropTypes.number,
  total: PropTypes.number,
  elements: PropTypes.arrayOf(PropTypes.object),
  imagePath: PropTypes.string
};

DataTable.defaultProps = {
  elements: []
};

export default DataTableContainer;
