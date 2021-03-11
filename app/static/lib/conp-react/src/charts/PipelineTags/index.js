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
        height: (9 / 16 * 100) + '%',
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
        text: 'Pipeline Representation By Tags'
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
            color: "#207EA0",
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
            }
        }
    },

    series: []

};

const PipelineTags = (props) => {

    const [chartData, setChartData] = useState()
    const [options, setOptions] = useState(defaultOptions);
    const [isLoading, setIsLoading] = useState(true)

    const [contextMenuOptions, setContextMenuOptions] = useState({});

    useEffect(() => {
        fetchChartData();
    }, [])

    const fetchChartData = async () => {

        try {
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

    const updateChart = (data) => {

        const pipelineData = Object.keys(data.pipelines).map(p => {
            return {
                name: p,
                value: data.pipelines[p]
            };
        });

        const series = [{
            name: 'Pipeline Tags',
            data: pipelineData
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
            pipelines: {}
        };

        chartData.pipelines.elements.forEach(pipeline => {

            if (!pipeline.tags.domain)
                return;

            if (!Array.isArray(pipeline.tags.domain)) {
                addOrIncreaseDatapoint(axes.pipelines, pipeline.tags.domain);
                return;
            }
            const tagsArr = pipeline.tags.domain;

            tagsArr.forEach(tag => {
                addOrIncreaseDatapoint(axes.pipelines, tag.toLowerCase());
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
                    const url = `/pipelines?tags=${e.target.point.name.toLowerCase()}`;
                    setContextMenuOptions({
                        title: e.target.point.name,
                        actionText: "View Pipelines",
                        style: style,
                        url: url,
                        show: true
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

export default PipelineTags;
