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
        text: 'Most Viewed Pages'
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
        name: 'Views',
        color: '#EA2627B3',
        data: [],
        yAxis: 0
    }]

};

const PageViews = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
            fetch('/analytics/views')
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

        Object.keys(axes.views).forEach(page => {
            xAxis.push(page);
            yAxis.push(axes.views[page]);
        });

        const series = [{
            name: 'Views',
            color: '#EA2627B3',
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
            if (element.label.includes('dataset?id=') && element.label !== 'dataset?id=projects') {
                axes.views[element.label] = element.nb_hits
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

export default PageViews;
