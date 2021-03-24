import React, { useState, useEffect } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'

import LoadingSpinner from "../LoadingSpinner"

const defaultOptions = {

    chart: {
        type: 'bar',
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Most Viewed Pipelines'
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

    series: []

};

const PipelinePageViews = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
            fetch('/analytics/pipelines/views')
                .then(res => res.json())
                .then(json => setChartData({
                    views: json
                }));

        } catch (err) {
            console.error(err);
        }
    };

    const updateChart = (axes) => {

        const xAxis = [];
        const yAxis = [];

        Object.keys(axes.views).some(page => {
            xAxis.push(page);
            yAxis.push(axes.views[page]);

            return xAxis.length >= 15
        });

        const series = [{
            name: 'Pipeline Views',
            color: '#207EA0B3',
            data: yAxis,
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

        if (!chartData) {
            return
        }

        const axes = {
            views: {}
        };

        chartData.views.forEach(element => {
            const title = element.title
            axes.views[title] = element.nb_hits
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

export default PipelinePageViews;
