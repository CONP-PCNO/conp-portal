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
                    <div className="col-xs-12 col-sm-6 col-md-3 col-lg-2 card-img card-social">
                      <img
                        alt="Project image"
                        className="card-img-top card-social-img"
                        src="/dataset_logo?id=projects/preventad-open"
                      />
                    </div>
                    <p className="card-description-subtitle">
                        Prevent-AD
                </p>
                    <p>
The PREVENT-AD (Pre-symptomatic Evaluation of Experimental or Novel Treatments for Alzheimer's Disease) cohort is composed of cognitively healthy participants over 55 years old, at risk of developing Alzheimer's Disease (AD) as their parents and/or siblings were/are affected by the disease. These ‘at-risk’ participants have been followed for a naturalistic study of the presymptomatic phase of AD since 2011 using multimodal measurements of various disease indicators. Two clinical trials intended to test pharmaco-preventive agents have also been conducted.

The PREVENT-AD research group is now releasing data openly with the intention of contributing to the community’s growing understanding of AD pathogenesis. 
                    </p>
                    <p>
                        Authors: StoP-AD Center - Douglas Mental Health University Institute
                </p>
                </div>
                <div className="d-flex mt-4 justify-content-end">
                    <a href={`/dataset?id=projects/preventad-open`}>
                        <button className="btn btn-outline-secondary"
                            type="button">
                            Read More
                            </button>
                    </a>
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
