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
        text: 'Most Searched Keywords'
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

const Keywords = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
            fetch('/analytics/keywords')
                .then(res => res.json())
                .then(json => setChartData({
                    keywords: json
                }));

        } catch (err) {
            console.error(err);
        }
    };

    const updateChart = (axes) => {

        const xAxis = [];
        const yAxis = [];

        Object.keys(axes.keywords).some(e => {
            xAxis.push(e);
            yAxis.push(axes.keywords[e]);

            return xAxis.length >= 15
        });

        const series = [{
            name: 'Keywords',
            color: '#88d368',
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
            keywords: {}
        };

        chartData.keywords.forEach(element => {
            axes.keywords[element.label] = element.nb_hits
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

export default Keywords;
