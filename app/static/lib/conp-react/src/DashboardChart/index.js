import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const DashboardChart = ({ datasetsURL, pipelinesURL, ...props }) => {

    const drawChart = (data) => {

        const xAxis = [];
        const yAxisDatasets = [];

        var countDatasets = 0;

        Object.keys(data.datasets).forEach(year => {
            Object.keys(data.datasets[year]).forEach(month => {
                countDatasets += data.datasets[year][month];
                xAxis.push(`${month}/${year}`);
                yAxisDatasets.push(countDatasets);
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
            }]

        })
    };

    const fetchElements = async () => {

        try {
            const res = await fetch(datasetsURL + '?elements=all');

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const datasetsRes = await res.json();

            const chartData = {
                datasets: {}
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
