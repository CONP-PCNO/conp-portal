import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const Spotlight = ({ datasetURL, ...props }) => {

    const [fetchedElements, setFetchedElements] = React.useState([]);

    const fetchElements = async () => {

        try {
            console.log(`Fetching from: ${datasetURL}`);
            const res = await fetch(datasetURL);

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const datasetRes = await res.json();

            console.log(JSON.stringify(datasetRes.elements[0]));
            setFetchedElements(datasetRes.elements);

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    useDebounce(() => void fetchElements(), 300, [datasetURL]);

    return (
        <div className="card-description">
            <h3 className="card-description-title">STUDY SPOTLIGHT</h3>
            <hr />

            <div className="card-description-text">
                <p className="card-description-subtitle">
                    {fetchedElements.length > 0 ? fetchedElements[0].title : ""}
                </p>
                <i>
                    {fetchedElements.length > 0 ? "StoP-AD Center - Douglas Mental Health University Institute" : ""}
                </i>
                <p>
                    {fetchedElements.length > 0 ? "Longitudinal multimodal study of pre-symptomatic Alzheimer's Disease" : ""}
                </p>
            </div>
            <div className="d-flex mt-4 justify-content-end">
                {fetchedElements.length > 0 ?
                    <a href={`/dataset?id=${fetchedElements[0].id}`}>
                        <button className="btn btn-outline-secondary"
                            type="button">
                            Read More
                            </button>
                    </a> : null}
            </div>
        </div>
    );
};

Spotlight.propTypes = {

};

Spotlight.defaultProps = {

};

export default Spotlight;
