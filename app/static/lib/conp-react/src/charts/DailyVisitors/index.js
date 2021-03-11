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

        Object.keys(axes.visitors).forEach(year => {
            Object.keys(axes.visitors[year]).forEach(month => {
                xAxis.push(`${month}/${year}`);
                yAxisVisitors.push(axes.visitors[year][month]);
            });
        });

        const series = [{
            name: 'Visitors',
            color: '#EA2627B3',
            data: yAxisVisitors,
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
