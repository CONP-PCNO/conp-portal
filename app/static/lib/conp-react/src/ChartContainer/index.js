import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";
import TotalDatasetsPipelines from '../charts/TotalDatasetsPipelines';
import DatasetModalities from '../charts/DatasetModalities';
import PipelineTags from '../charts/PipelineTags'

class ChartContainer extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            datasets: null,
            pipelines: null,
            toggle: 1
        };

        this.toggleChart = this.toggleChart.bind(this);
    }

    componentDidMount() {
        this.fetchElements();
    }

    async fetchElements() {

        try {
            const datasetsFetch = await fetch(this.props.datasetsURL + '?elements=all');

            if (!datasetsFetch.ok) {
                throw new Error(
                    `Request failed with status: ${datasetsFetch.status} (${datasetsFetch.statusText})`
                );
            }

            const datasetsRes = await datasetsFetch.json();

            const pipelinesFetch = await fetch(this.props.pipelinesURL);

            if (!pipelinesFetch.ok) {
                throw new Error(
                    `Request failed with status: ${pipelinesFetch.status} (${pipelinesFetch.statusText})`
                );
            }

            const pipelinesRes = await pipelinesFetch.json();

            this.setState({
                datasets: datasetsRes,
                pipelines: pipelinesRes
            })

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    renderChart(toggle) {
        switch (toggle) {
            case 1:
                return <TotalDatasetsPipelines
                    datasets={this.state.datasets}
                    pipelines={this.state.pipelines} />;
            case 2:
                return <DatasetModalities
                    datasets={this.state.datasets}
                    pipelines={this.state.pipelines} />;
            case 3:
                return <PipelineTags
                    pipelines={this.state.pipelines} />;
            default:
                return <TotalDatasetsPipelines
                    datasets={this.state.datasets}
                    pipelines={this.state.pipelines} />;
        }
    }

    toggleChart(event, number) {
        event.preventDefault();
        this.setState({
            toggle: number
        });
    }

    render() {
        return (
            <div>
                <div className="d-flex flex-row-reverse">
                    <div className="dropdown show" style={{ zIndex: 1 }}>
                        <a className="btn btn-secondary btn-sm dropdown-toggle" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            Select Chart
                        </a>

                        <div className="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuLink">
                            <button className="dropdown-item" type="button" onClick={(e) => {this.toggleChart(e, 1)}}>Total Datasets and Pipelines</button>
                            <button className="dropdown-item" type="button" onClick={(e) => {this.toggleChart(e, 2)}}>Dataset Modalities</button>
                            <button className="dropdown-item" type="button" onClick={(e) => {this.toggleChart(e, 3)}}>Pipeline Tags</button>
                        </div>
                    </div>
                </div>
                {this.renderChart(this.state.toggle)}
            </div>
        );
    }

};

ChartContainer.propTypes = {

};

ChartContainer.defaultProps = {

};

export default ChartContainer;
