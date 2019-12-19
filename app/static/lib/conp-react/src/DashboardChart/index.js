import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const DashboardChart = ({ datasetsURL, pipelinesURL, ...props }) => {

    const drawChart = (data) => {
        console.log('drawing chart');

        const xAxis = [];
        const yAxisDatasets = [];
        const yAxisPipelines = [];

        var countDatasets = 0;
        var countPipelines = 0;

        Object.keys(data.datasets).forEach(year => {
            Object.keys(data.datasets[year]).forEach(month => {
                countDatasets += data.datasets[year][month];
                if(data.pipelines[year][month]){
                    countPipelines += data.pipelines[year][month];
                }
                xAxis.push(`${month}/${year}`);
                yAxisDatasets.push(countDatasets);
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
                text: 'Cumulative Number of Datasets and Pipelines in 2019'
            },

            yAxis: [{
                title: {
                    text: 'Number of Datasets'
                }
            }, {
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
                name: 'Datasets',
                data: yAxisDatasets
            }, {
                name: 'Pipelines',
                data: yAxisPipelines,
                yAxis: 1
            }]

        })
    };

    const fetchElements = async () => {

        try {
            const res = await fetch(datasetsURL);

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const datasetsRes = await res.json();

            const chartData = {
                datasets: {
                    2019:{
                        1: 0,
                        2: 0,
                        3: 0,
                        4: 0,
                        5: 0,
                        6: 0,
                        7: 0,
                        8: 0,
                        9: 0,
                        10: 0,
                        11: 0,
                        12: 0,
                    }
                },
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

            const pipelines = await fetch(pipelinesURL);

            if (!pipelines.ok) {
                throw new Error(
                    `Request failed with status: ${pipelines.status} (${pipelines.statusText})`
                );
            }

            const pipelinesRes = await pipelines.json();

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
