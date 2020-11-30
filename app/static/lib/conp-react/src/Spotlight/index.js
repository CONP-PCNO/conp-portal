import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const Spotlight = ({ datasetURL, ...props }) => {

    const [fetchedElements, setFetchedElements] = React.useState([]);

    const fetchElements = async () => {

        try {
            const res = await fetch(datasetURL);

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const datasetRes = await res.json();

            setFetchedElements(datasetRes.elements);

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    //useDebounce(() => void fetchElements(), 300, [datasetURL]);

    return (
        //fetchedElements.length > 0 ?
            <div className="card-description">
                <h3 className="card-description-title">STUDY SPOTLIGHT</h3>
                <hr />

                <div className="card-description-text">
                    <div className="card-img d-flex justify-content-center">
                      <img
                        alt="Project image"
                        className="img-fluid"
                        src="/dataset_logo?id=projects/preventad-registered"
                      />
                    </div>
                    <p className="card-description-subtitle">
                        PREVENT-AD Datasets
                    </p>
                    <p>
The PREVENT-AD (Pre-symptomatic Evaluation of Experimental or Novel Treatments for Alzheimer's Disease) cohort is composed
of cognitively healthy participants over 55 years old, at risk of developing Alzheimer's Disease (AD) as their parents
and/or siblings were/are affected by the disease. These ‘at-risk’ participants have been followed for a naturalistic study
of the presymptomatic phase of AD since 2011 using multimodal measurements of various disease indicators. One clinical
trial intended to test a pharmaco-preventive agent has also been conducted.
                    </p>
                    <p>
The PREVENT-AD dataset is available to researchers around the world with the intention to contribute to the community’s
growing understanding of AD pathogenesis.
                    </p>
                </div>
                <div className="d-flex mt-4 justify-content-around">
                    <div>
                        <a href={`/dataset?id=projects/preventad-open`}>
                            <button className="btn btn-outline-secondary" type="button">
                              Open Dataset
                            </button>
                        </a>
                    </div>
                    <div>
                        <a href={`/dataset?id=projects/preventad-open-bids`}>
                            <button className="btn btn-outline-secondary" type="button">
                              Open Dataset (BIDS)
                            </button>
                        </a>
                    </div>
                    <div>
                        <a href={`/dataset?id=projects/preventad-registered`}>
                            <button className="btn btn-outline-secondary" type="button">
                                Registered Dataset
                            </button>
                        </a>
                    </div>
                </div>
                <div className="card-description-subtitle">
                    <p>
                        Authors: StoP-AD Center - Douglas Mental Health University Institute
                    </p>
                </div>
            </div>
            //: null
    );
};

Spotlight.propTypes = {

};

Spotlight.defaultProps = {

};

export default Spotlight;
