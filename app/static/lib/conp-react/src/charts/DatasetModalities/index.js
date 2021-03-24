import React, { useState, useEffect } from "react";
import ContextMenu from '../ContextMenu'
import LoadingSpinner from "../LoadingSpinner"

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official';
require('highcharts/highcharts-more.js')(Highcharts);
require('highcharts-custom-events')(Highcharts);

const defaultOptions = {

    chart: {
        type: 'packedbubble',
        backgroundColor: '#FFF',
        margin: [-30, -30, -30, -30],
        colors: ["#EA2627", "#A5A5A5", "#FFC000", "#207EA0", "#898989", "#5E5E5E"]
    },
    credits: {
        enabled: false
    },
    legend: {
        enabled: false
    },
    title: {
        text: 'Dataset Modalities Representation By Keywords'
    },

    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value}'
    },

    plotOptions: {
        series: {
            allowPointSelect: true,
            point: {
                events: {}
            }
        },

        packedbubble: {
            color: "#EA2627",
            minSize: '30%',
            maxSize: '100%',
            zMin: 0,
            zMax: 20,
            layoutAlgorithm: {
                initialPositions: 'random',
                bubblePadding: 12,
                gravitationalConstant: 0.006,
                splitSeries: false,
            },
            dataLabels: {
                enabled: true,
                format: '{point.name}',
                filter: {
                    property: 'y',
                    operator: '>',
                    value: 0
                },
                style: {
                    color: 'black',
                    textOutline: 'none',
                    fontWeight: 'normal'
                }
            },
            allowPointSelect: true
        }
    },

    series: []

};

const DatasetModalities = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true);

    const [contextMenuOptions, setContextMenuOptions] = useState({});

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

        } catch (err) {
            console.error(err);
        }
    };

    const updateChart = (data) => {

        const datasetData = Object.keys(data.datasets).map(d => {
            return {
                name: d,
                value: data.datasets[d]
            };
        });

        const series = [{
            name: 'Dataset Modalities',
            data: datasetData
        }];

        setOptions(prevOptions => ({
            ...prevOptions,
            series: series,
        }));

        setIsLoading(false);
    };

    useEffect(() => {

        if (!chartData) {
            return
        }

        const axes = {
            datasets: {}
        };

        chartData.datasets.elements.forEach(dataset => {

            if (!dataset.modalities)
                return;

            dataset.modalities.forEach(modality => {
                addOrIncreaseDatapoint(axes.datasets, modality.toLowerCase());
            })
        })

        updateChart(axes);

    }, [chartData]);

    const addOrIncreaseDatapoint = (data, point) => {
        if (!Object.keys(data).includes(point)) {
            data[point] = 1;
        }
        else {
            data[point] += 1;
        }
    }

    useEffect(() => {
        setOptions(prevOptions => {
            const options = prevOptions
            options.plotOptions.series.point.events = {
                contextmenu: function (e) {
                    e.preventDefault()
                    console.log(e.target)
                    const xPos = e.pageX;
                    const yPos = e.pageY;
                    const style = {
                        "position": "absolute",
                        "left": xPos,
                        "top": yPos,
                        "zIndex": 1000
                    };
                    const url = `/search?modalities=${e.target.point.name.toLowerCase()}`;
                    setContextMenuOptions({
                        title: e.target.point.name,
                        actionText: "View Datasets",
                        style: style,
                        url: url
                    })
                }
            }
            return options
        })
    }, []);

    return (
        isLoading ?
            <LoadingSpinner />
            :
            <div>
                <ContextMenu options={contextMenuOptions} />
                <HighchartsReact
                    highcharts={Highcharts}
                    options={options}
                />
            </div>
    );
};

export default DatasetModalities;
