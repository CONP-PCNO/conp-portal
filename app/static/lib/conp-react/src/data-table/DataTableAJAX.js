import React from "react";
import PropTypes from "prop-types";

import DataTable from "./DataTable";

const DataTableAJAX = ({ baseURL, ...props }) => {
  return <DataTable {...props} />;
};

DataTableAJAX.propTypes = {
  baseURL: PropTypes.string
};

DataTable.defaultProps = {};

export default DataTableAJAX;
