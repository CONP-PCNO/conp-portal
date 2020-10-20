import React, { useState } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'

const defaultOptions = {

    chart: {
        type: 'column',
        styledMode: true,
        backgroundColor: '#FFF'
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Cumulative Number of Datasets and Pipelines'
    },

    yAxis: [{
        title: {
            text: '',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        allowDecimals: false,
    }],

    xAxis: {
        categories: []
    },

    plotOptions: {
        column: {
            borderRadius: 5
        }
    },

    series: [{
        name: 'Datasets',
        data: [],
        yAxis: 0
    },
    {
        name: 'Pipelines',
        data: [],
        yAxis: 0
    }]

};

const TotalDatasetsPipelines = ({ datasets, pipelines, ...props }) => {

    const [options, setOptions] = useState(defaultOptions);
    const [isDrawn, setIsDrawn] = useState(false);

    const updateChart = (data) => {

        const xAxis = [];
        const yAxisDatasets = [];
        const yAxisPipelines = [];

        var countDatasets = 0;
        var countPipelines = 0;

        Object.keys(data.datasets).forEach(year => {
            Object.keys(data.datasets[year]).forEach(month => {
                xAxis.push(`${month}/${year}`);
                countDatasets += data.datasets[year][month];
                yAxisDatasets.push(countDatasets);
            });
        });

        Object.keys(data.pipelines).forEach(year => {
            Object.keys(data.pipelines[year]).forEach(month => {
                countPipelines += data.pipelines[year][month];
                yAxisPipelines.push(countPipelines);
            });
        });

        /* Only show pipeline data for the months we have dataset data */
        var yAxisPipelinesExtract = yAxisPipelines;
        if (yAxisDatasets.length > yAxisPipelines.length) {
            yAxisPipelinesExtract = new Array(yAxisDatasets.length - yAxisPipelines.length).fill(0).concat(yAxisPipelines);
        }
        else if (yAxisDatasets.length < yAxisPipelines.length) {
            yAxisPipelinesExtract = yAxisPipelines.slice(Math.max(yAxisPipelines.length - xAxis.length, 0));
        }

        const series = [{
            name: 'Datasets',
            data: yAxisDatasets,
            yAxis: 0
        },
        {
            name: 'Pipelines',
            data: yAxisPipelinesExtract,
            yAxis: 0
        }];

        setOptions(prevOptions => ({
            ...prevOptions,
            series: series,
            xAxis: {
                categories: xAxis
            }
        }));

    };

    const constructData = () => {

        const chartData = {
            datasets: {},
            pipelines: {}
        };

        datasets.elements.forEach(element => {
            const dateAdded = new Date(element.dateAdded);

            if (!chartData.datasets[dateAdded.getFullYear()]) {
                chartData.datasets[dateAdded.getFullYear()] = {}
            }

            if (!chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
            }
            else {
                chartData.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
            }
        });

        /* check if we've skipped months */

        var months = [];

        for (var i = 1; i <= 12; i++) {
            months.push(i);
        }

        const today = new Date();

        Object.keys(chartData.datasets).forEach(year => {
            for (var i = 1; i <= 12; i++) {
                if (year === today.getFullYear() && i === today.getMonth() + 2) {
                    break;
                }
                if (Object.keys(chartData.datasets).includes((year - 1).toString()) &&
                    !Object.keys(chartData.datasets[year]).includes(`${i}`) && i === 1) {
                    chartData.datasets[year][i] = 0;
                }
                if (Object.keys(chartData.datasets[year]).includes(`${i - 1}`) &&
                    !Object.keys(chartData.datasets[year]).includes(`${i}`)) {
                    chartData.datasets[year][i] = 0;
                }
            }
        });

        pipelines.elements.forEach(element => {
            const dateAdded = new Date(element.publicationdate);

            if (!chartData.pipelines[dateAdded.getFullYear()]) {
                chartData.pipelines[dateAdded.getFullYear()] = {}
            }

            if (!chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
            }
            else {
                chartData.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
            }
        });

        Object.keys(chartData.pipelines).forEach(year => {
            for (var i = 1; i <= 12; i++) {
                if (year === today.getFullYear() && i === today.getMonth() + 2) {
                    break;
                }
                if (Object.keys(chartData.pipelines).includes((year - 1).toString()) &&
                    !Object.keys(chartData.pipelines[year]).includes(`${i}`) && i === 1) {
                    chartData.pipelines[year][i] = 0;
                }
                if (Object.keys(chartData.pipelines[year]).includes(`${i - 1}`) &&
                    !Object.keys(chartData.pipelines[year]).includes(`${i}`)) {
                    chartData.pipelines[year][i] = 0;
                }
            }
        });

        updateChart(chartData);

    };

    if (datasets && pipelines && !isDrawn) {
        constructData();
        setIsDrawn(true);
    }

    return (
        <HighchartsReact
            highcharts={Highcharts}
            options={options}
        />
    );
};

TotalDatasetsPipelines.propTypes = {

};

TotalDatasetsPipelines.defaultProps = {

};

export default TotalDatasetsPipelines;
