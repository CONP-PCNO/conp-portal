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
        text: 'Number of Unique Visitors'
    },

    yAxis: [{ // Primary yAxis
        title: {
            text: 'Cumulative Visitors',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        labels: {
            format: '{value}',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        allowDecimals: false,
        opposite: true
    }, { // Secondary yAxis
        labels: {
            format: '{value}',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        title: {
            text: 'Visitors',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        allowDecimals: false
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
        name: 'Visitors',
        color: '#EA2627B3',
        data: [],
        yAxis: 0
    }]

};

const DailyVisitors = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
            fetch('/analytics/visitors')
                .then(res => res.json())
                .then(json => setChartData({
                    visitors: json
                }));

        } catch (err) {
            console.error(err);
        }
    };

    const updateChart = (axes) => {

        const xAxis = [];
        const yAxisVisitors = [];
        const yAxisCumulativeVisitors = [];

        let cumulativeVisitors = 0;

        Object.keys(axes.visitors).forEach(year => {
            Object.keys(axes.visitors[year]).forEach(month => {
                xAxis.push(`${month}/${year}`);
                yAxisVisitors.push(axes.visitors[year][month]);

                cumulativeVisitors += axes.visitors[year][month]
                yAxisCumulativeVisitors.push(cumulativeVisitors);
            });
        });

        const series = [{
            name: 'Cumulative Visitors',
            color: '#88d368',
            type: 'column',
            data: yAxisCumulativeVisitors,
            yAxis: 0
        },
        {
            name: 'Visitors',
            color: '#207EA0B3',
            type: 'spline',
            data: yAxisVisitors,
            yAxis: 1
        }
        ];

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
            visitors: {}
        };

        chartData.visitors.forEach(element => {
            const dateOfVisit = new Date(element.date);

            if (!axes.visitors[dateOfVisit.getFullYear()]) {
                axes.visitors[dateOfVisit.getFullYear()] = {}
            }

            if (!axes.visitors[dateOfVisit.getFullYear()][dateOfVisit.getMonth() + 1]) {
                axes.visitors[dateOfVisit.getFullYear()][dateOfVisit.getMonth() + 1] = element.nb_uniq_visitors;
            }
            else {
                axes.visitors[dateOfVisit.getFullYear()][dateOfVisit.getMonth() + 1] += element.nb_uniq_visitors
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

export default DailyVisitors;
