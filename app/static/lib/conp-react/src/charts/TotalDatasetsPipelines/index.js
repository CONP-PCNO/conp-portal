import React, { useState, useEffect } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'

import LoadingSpinner from "../LoadingSpinner"

const defaultOptions = {

    chart: {
        type: 'column',
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
        color: '#EA2627B3',
        data: [],
        yAxis: 0
    },
    {
        name: 'Pipelines',
        color: '#207EA0B3',
        data: [],
        yAxis: 0
    }]

};

const TotalDatasetsPipelines = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
            fetch('/dataset-search?elements=all')
                .then(res => res.json())
                .then(json => setChartData(prevState => ({
                    ...prevState,
                    datasets: json
                })));

            fetch('/pipeline-search')
                .then(res => res.json())
                .then(json => setChartData(prevState => ({
                    ...prevState,
                    pipelines: json
                })));

        } catch (err) {
            console.error(err);
        }
    };

    const updateChart = (axes) => {

        const xAxis = [];
        const yAxisDatasets = [];
        const yAxisPipelines = [];

        var countDatasets = 0;
        var countPipelines = 0;

        Object.keys(axes.datasets).forEach(year => {
            Object.keys(axes.datasets[year]).forEach(month => {
                xAxis.push(`${month}/${year}`);
                countDatasets += axes.datasets[year][month];
                yAxisDatasets.push(countDatasets);
            });
        });

        Object.keys(axes.pipelines).forEach(year => {
            Object.keys(axes.pipelines[year]).forEach(month => {
                countPipelines += axes.pipelines[year][month];
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
            color: '#EA2627B3',
            data: yAxisDatasets,
            yAxis: 0
        },
        {
            name: 'Pipelines',
            color: '#207EA0B3',
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

        setIsLoading(false);

    };

    useEffect(() => {

        if (!chartData || !chartData.datasets || !chartData.pipelines) {
            return
        }

        const axes = {
            datasets: {},
            pipelines: {}
        };

        chartData.datasets.elements.forEach(element => {
            const dateAdded = new Date(element.dateAdded);

            if (!axes.datasets[dateAdded.getFullYear()]) {
                axes.datasets[dateAdded.getFullYear()] = {}
            }

            if (!axes.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                axes.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
            }
            else {
                axes.datasets[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
            }
        });

        /* check if we've skipped months */

        var months = [];

        for (var i = 1; i <= 12; i++) {
            months.push(i);
        }

        const today = new Date();

        if (!Object.keys(axes.datasets).includes(today.getFullYear())) {
            axes.datasets[today.getFullYear()] = {}
        }

        if (!Object.keys(axes.pipelines).includes(today.getFullYear())) {
            axes.pipelines[today.getFullYear()] = {}
        }

        Object.keys(axes.datasets).forEach(year => {
            for (var i = 1; i <= 12; i++) {
                if (parseInt(year) === today.getFullYear() && i === (today.getMonth() + 2)) {
                    break;
                }
                if (Object.keys(axes.datasets).includes((year - 1).toString()) &&
                    !Object.keys(axes.datasets[year]).includes(`${i}`) && i === 1) {
                    axes.datasets[year][i] = 0;
                }
                if (Object.keys(axes.datasets[year]).includes(`${i - 1}`) &&
                    !Object.keys(axes.datasets[year]).includes(`${i}`)) {
                    axes.datasets[year][i] = 0;
                }
            }
        });

        chartData.pipelines.elements.forEach(element => {
            const dateAdded = new Date(element.publicationdate);

            if (!axes.pipelines[dateAdded.getFullYear()]) {
                axes.pipelines[dateAdded.getFullYear()] = {}
            }

            if (!axes.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1]) {
                axes.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] = 1;
            }
            else {
                axes.pipelines[dateAdded.getFullYear()][dateAdded.getMonth() + 1] += 1
            }
        });

        Object.keys(axes.pipelines).forEach(year => {
            for (var i = 1; i <= 12; i++) {
                if (year === today.getFullYear() && i === today.getMonth() + 2) {
                    break;
                }
                if (Object.keys(axes.pipelines).includes((year - 1).toString()) &&
                    !Object.keys(axes.pipelines[year]).includes(`${i}`) && i === 1) {
                    axes.pipelines[year][i] = 0;
                }
                if (Object.keys(axes.pipelines[year]).includes(`${i - 1}`) &&
                    !Object.keys(axes.pipelines[year]).includes(`${i}`)) {
                    axes.pipelines[year][i] = 0;
                }
            }
        });

        updateChart(axes);

    }, [chartData])

    return (
        isLoading ?
            <LoadingSpinner />
            :
            <HighchartsReact
                highcharts={Highcharts}
                options={options}
            />
    );
};

export default TotalDatasetsPipelines;
