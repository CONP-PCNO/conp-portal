import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const DashboardChart = ({ datasetsURL, pipelinesURL, ...props }) => {

    //const [fetchedElements, setFetchedElements] = React.useState([]);
    //const [totalState, setTotalState] = React.useState(0);

    const drawChart = (data) => {
        console.log('drawing chart');

        const xAxis = [];
        const yAxisDatasets = [];
        const yAxisPipelines = [];

        Object.keys(data.datasets).forEach(year => {
            Object.keys(data.datasets[year]).forEach(month => {
                xAxis.push(`${month}/${year}`);
                yAxisDatasets.push(data.datasets[year][month]);
                yAxisPipelines.push(data.pipelines[year][month] ? data.pipelines[year][month] : 0);
            });
        });

        console.log(xAxis);
        console.log(yAxisDatasets);
        console.log(yAxisPipelines);

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
                text: 'Number of Datasets and Pipelines in 2019'
            },

            yAxis: [{
                className: 'highcharts-color-0',
                title: {
                    text: 'Number of Datasets'
                }
            }, {
                className: 'highcharts-color-1',
                opposite: true,
                title: {
                    text: 'Number of Pipelines'
                }
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
                name: 'CONP Datasets',
                data: yAxisDatasets
            }, {
                name: 'CONP Pipelines',
                data: yAxisPipelines,
                yAxis: 1
            }]

        })
    };

    const fetchElements = async () => {

        try {
            console.log(`Fetching from: ${datasetsURL}`);
            const res = await fetch(datasetsURL);

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const datasetsRes = await res.json();

            console.log(JSON.stringify(datasetsRes));

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
            })

            console.log(chartData);

            console.log(`Fetching from: ${pipelinesURL}`);
            const pipelines = await fetch(pipelinesURL);

            if (!pipelines.ok) {
                throw new Error(
                    `Request failed with status: ${pipelines.status} (${pipelines.statusText})`
                );
            }

            const pipelinesRes = await pipelines.json();

            console.log(JSON.stringify(pipelinesRes));

            chartData.pipelines[2019] = {};

            chartData.pipelines[2019][12] = pipelinesRes.elements.length;

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
