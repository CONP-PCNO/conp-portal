import React, { useState, useEffect } from "react";
import TotalDatasetsPipelines from '../charts/TotalDatasetsPipelines';
import DatasetModalities from '../charts/DatasetModalities';
import PipelineTags from '../charts/PipelineTags'

const ChartContainer = (props) => {

    const [showToggle, setShowToggle] = useState(props.showToggle || false)
    const [toggleState, setToggleState] = useState(props.toggleState || 1)

    const renderChart = () => {
        switch (toggleState) {
            case 1:
                return <TotalDatasetsPipelines />;
            case 2:
                return <DatasetModalities />;
            case 3:
                return <PipelineTags />;
            default:
                return <TotalDatasetsPipelines />;
        }
    }

    return (
        <div style={{ minHeight: "300px" }}>
            {showToggle ? <div className="d-flex flex-row-reverse">
                <div className="dropdown show mt-2 mr-2" style={{ zIndex: 1 }}>
                    <button className="btn btn-secondary btn-sm dropdown-toggle" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Select Chart
                        </button>

                    <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuLink">
                        <button className="dropdown-item" type="button" onClick={setToggleState(1)}>Total Datasets and Pipelines</button>
                        <button className="dropdown-item" type="button" onClick={setToggleState(2)}>Dataset Modalities</button>
                        <button className="dropdown-item" type="button" onClick={setToggleState(3)}>Pipeline Tags</button>
                    </div>
                </div>
            </div> : null}

            {renderChart()}
        </div>
    );

};

export default ChartContainer;
