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
                data: [0, 0, 0, data.datasetsTotal]
            }, {
                name: 'CONP Pipelines',
                data: [0, 0, 0, data.pipelinesTotal],
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

            console.log(JSON.stringify(datasetsRes.total));

            //setFetchedElements(parsed.elements);
            //setTotalState(parsed.total);

            console.log(`Fetching from: ${pipelinesURL}`);
            const pipelines = await fetch(pipelinesURL);

            if (!pipelines.ok) {
                throw new Error(
                    `Request failed with status: ${pipelines.status} (${pipelines.statusText})`
                );
            }

            const pipelinesRes = await pipelines.json();

            console.log(JSON.stringify(pipelinesRes.elements.length));

            const data = {
                datasetsTotal: datasetsRes.total,
                pipelinesTotal: pipelinesRes.elements.length
            };

            drawChart(data);

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
