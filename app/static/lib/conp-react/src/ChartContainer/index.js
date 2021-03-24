import React, { useState, useEffect } from "react";
import TotalDatasetsPipelines from '../charts/TotalDatasetsPipelines';
import DatasetModalities from '../charts/DatasetModalities';
import PipelineTags from '../charts/PipelineTags';
import DailyVisitors from "../charts/DailyVisitors";
import DatasetPageViews from "../charts/DatasetPageViews";
import PipelinePageViews from "../charts/PipelinePageViews";
import Keywords from "../charts/Keywords";

const ChartContainer = (props) => {

    const [showToggle, setShowToggle] = useState(props.showToggle || false)
    const [toggleState, setToggleState] = useState(props.toggleState)

    const renderChart = () => {
        switch (toggleState) {
            case "TotalDatasetsPipelines":
                return <TotalDatasetsPipelines />;
            case "DatasetModalities":
                return <DatasetModalities />;
            case "PipelineTags":
                return <PipelineTags />;
            case "DailyVisitors":
                return <DailyVisitors />;
            case "DatasetPageViews":
                return <DatasetPageViews />;
            case "PipelinePageViews":
                return <PipelinePageViews />;
            case "Keywords":
                return <Keywords />;
            default:
                return <TotalDatasetsPipelines />;
        }
    }

    return (
        <div style={{ minHeight: "360px" }}>
            {showToggle ? <div className="d-flex flex-row-reverse">
                <div className="dropdown show mt-2 mr-2" style={{ zIndex: 1 }}>
                    <button className="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Select Chart
                        </button>

                    <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuLink">
                        <button className="dropdown-item" type="button" onClick={setToggleState("TotalDatasetsPipelines")}>Total Datasets and Pipelines</button>
                        <button className="dropdown-item" type="button" onClick={setToggleState("DatasetModalities")}>Dataset Modalities</button>
                        <button className="dropdown-item" type="button" onClick={setToggleState("PipelineTags")}>Pipeline Tags</button>
                    </div>
                </div>
            </div> : null}

            {renderChart()}
        </div>
    );

};

export default ChartContainer;
