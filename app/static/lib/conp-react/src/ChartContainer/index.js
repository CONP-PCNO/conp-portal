import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";
import TotalDatasetsPipelines from '../charts/TotalDatasetsPipelines'

class ChartContainer extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            datasets: null,
            pipelines: null
        };
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

            this.setState({
                datasets: datasetsRes
            })

            const pipelinesFetch = await fetch(this.props.pipelinesURL);

            if (!pipelinesFetch.ok) {
                throw new Error(
                    `Request failed with status: ${pipelinesFetch.status} (${pipelinesFetch.statusText})`
                );
            }

            const pipelinesRes = await pipelinesFetch.json();

            this.setState({
                pipelines: pipelinesRes
            })

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    render () {
        return (
            this.state.datasets && this.state.pipelines ?
            <TotalDatasetsPipelines
                datasets={this.state.datasets}
                pipelines={this.state.pipelines}
            />
            : null
        );
    }
    
};

ChartContainer.propTypes = {

};

ChartContainer.defaultProps = {

};

export default ChartContainer;
