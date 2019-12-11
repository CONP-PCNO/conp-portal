import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const DashboardChart = ({ endpointURL, ...props }) => {

    const [fetchedElements, setFetchedElements] = React.useState([]);
    const [totalState, setTotalState] = React.useState(0);

    const drawChart = (total) => {
        console.log('drawing chart');
        console.log('totalState is ' + totalState);
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
                    text: 'Number of Pipelines'
                }
            }, {
                className: 'highcharts-color-1',
                opposite: true,
                title: {
                    text: 'Number of Datasets'
                }
            }],

            xAxis: {
                categories: ["January'19", "February'19", "March'19", "April'19"]
            },

            plotOptions: {
                column: {
                    borderRadius: 5
                }
            },



            series: [{
                name: 'CONP Datasets',
                data: [0, 0, 0, total]
            }, {
                name: 'CONP Pipelines',
                data: [0, 0, 0, 8],
                yAxis: 1
            }]

        })
    };

    const fetchElements = async () => {

        const url = endpointURL;

        console.log(`Fetching from: ${url}`);

        try {
            const res = await fetch(url);

            if (!res.ok) {
                throw new Error(
                    `Request failed with status: ${res.status} (${res.statusText})`
                );
            }

            const parsed = await res.json();

            console.log(JSON.stringify(parsed.total));

            setFetchedElements(parsed.elements);
            setTotalState(parsed.total);

            drawChart(parsed.total);

        } catch (err) {
            alert("There was an error retrieving the search results.");
            console.error(err);
        }
    };

    useDebounce(() => void fetchElements(), 300, [endpointURL]);

    return (
        <div id="dashboard-chart" />
    );
};

DashboardChart.propTypes = {

};

DashboardChart.defaultProps = {

};

export default DashboardChart;
