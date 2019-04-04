import React from "react";
import PropTypes from "prop-types";

const DataTable = ({
  authorized,
  elements,
  renderElement,
  query,
  setQuery
}) => {
  return (
    <div className="search-dataset-table" cellSpacing={0}>
      <div className="search-dataset-toolbar">SEARCH TOOLBAR</div>
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
      <div className="search-dataset-toolbar">PAGE PARAMS</div>
    </div>
  );
};

DataTable.propTypes = {
  authorized: PropTypes.bool,
  elements: PropTypes.arrayOf(PropTypes.object),
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

export default DataTable;
