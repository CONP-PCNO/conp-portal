import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import * as qs from "query-string";

import DatasetElement from "../DatasetElement";
import PipelineElement from "../PipelineElement";

const ElementContainer = ({ element, elementProps, complementUrl }) => {
  const [activeCbrainIdState, setActiveCbrainIdState] = useState("");
  const [cbrainIdsState, setCbrainIdsState] = useState([]);

  const fetchCbrainIds = async () => {
    const url = `${complementUrl}?${qs.stringify(
      { max_per_page: "All", cbrain: true },
      { arrayFormat: "comma" }
    )}`;
    try {
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(
          `Request failed with status: ${res.status} (${res.statusText})`
        );
      }

      const parsed = await res.json();

      setCbrainIdsState(
        parsed.elements.map((element) => {
          return element.platforms
            ? {
                url: element.platforms[0].uri,
                id: element.id,
                title: element.title,
              }
            : { url: element.cbrain_id, id: element.id, title: element.title };
        })
      );
    } catch (err) {
      alert("There was an error populating the CBRAIN options.");
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCbrainIds();
  }, []);
  const updateActiveCbrainId = (elementId, activeValue) => {
    setActiveCbrainIdState(activeValue)
  };

  return React.createElement(element, {
    ...elementProps,
    cbrainIds: cbrainIdsState,
    activeCbrainId: activeCbrainIdState,
    updateActiveCbrainId: updateActiveCbrainId,
  });
};

ElementContainer.propTypes = {
  element: PropTypes.oneOfType([
    PropTypes.instanceOf(DatasetElement),
    PropTypes.instanceOf(PipelineElement),
  ]),
  elementProps: PropTypes.object,
  complementUrl: PropTypes.string,
};

export default ElementContainer;
