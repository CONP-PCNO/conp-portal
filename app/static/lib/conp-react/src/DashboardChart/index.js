import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const DashboardChart = ({ datasetsURL, pipelinesURL, ...props }) => {

    const drawChart = (data) => {

        const xAxis = [];
        const yAxisDatasets = [];
        const yAxisPipelines = [];

        var countDatasets = 0;
        var countPipelines = 0;

        Object.keys(data.datasets).forEach(year => {
            Object.keys(data.datasets[year]).forEach(month => {
                countDatasets += data.datasets[year][month];
                xAxis.push(`${month}/${year}`);
                yAxisDatasets.push(countDatasets);
            });
        });

        Object.keys(data.pipelines).forEach(year => {
            Object.keys(data.pipelines[year]).forEach(month => {
                countPipelines += data.pipelines[year][month];
                yAxisPipelines.push(countPipelines);
            });
        });

        Highcharts.chart('dashboard-chart-container', {

            chart: {
                type: 'column',
                styledMode: true,
                backgroundColor: '#FFF'
            },
            credits: {
                enabled: false
            },

            title: {
                text: 'Cumulative Number of Datasets'
            },

            yAxis: [{
                title: {
                    text: 'Number of Datasets'
                },
                allowDecimals: false,
            }],

            xAxis: {
                categories: xAxis
            },

            plotOptions: {
                column: {
                    borderRadius: 5
                }
            },

            series: [{
                name: 'Datasets',
                data: yAxisDatasets
            },
            {
                name: 'Pipelines',
                data: yAxisPipelines
            }]

        })
    };

    const fetchElements = async () => {

        try {
            const datasetsFetch = await fetch(datasetsURL + '?elements=all');

            if (!datasetsFetch.ok) {
                throw new Error(
                    `Request failed with status: ${datasetsFetch.status} (${datasetsFetch.statusText})`
                );
            }

            const datasetsRes = await datasetsFetch.json();

            const pipelinesFetch = await fetch(pipelinesURL);

            if (!pipelinesFetch.ok) {
                throw new Error(
                    `Request failed with status: ${pipelinesFetch.status} (${pipelinesFetch.statusText})`
                );
            }

            const pipelinesRes = await pipelinesFetch.json();

            const chartData = {
                datasets: {},
                pipelines: {}
            };

            datasetsRes.elements.map(element => {
                const dateAdded = new Date(element.dateAdded);

                if(!chartData.datasets[dateAdded.getFullYear()]){
                    chartData.datasets[dateAdded.getFullYear()] = {}
                }

                if (!chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                    chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
                }
                else {
                    chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
                }
            });

            pipelinesRes.elements.map(element => {
                const dateAdded = new Date(element.publicationdate);

                if(!chartData.pipelines[dateAdded.getFullYear()]){
                    chartData.pipelines[dateAdded.getFullYear()] = {}
                }

                if (!chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                    chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
                }
                else {
                    chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
                }
            })

            drawChart(chartData);

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    useDebounce(() => void fetchElements(), 300, [datasetsURL]);

    return (
        <div id="dashboard-chart" />
    );
};

DashboardChart.propTypes = {

};

DashboardChart.defaultProps = {

};

export default DashboardChart;
