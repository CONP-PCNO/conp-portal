import React, { useState } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'
require('highcharts/highcharts-more.js')(Highcharts);

const defaultOptions = {

    chart: {
        type: 'packedbubble',
        backgroundColor: '#FFF',
        height: '100%',
        spacing: [0, 0, 0, 0],
        margin: [0, 0, 0, 0]
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Pipeline Tags'
    },

    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value}'
    },

    plotOptions: {
        packedbubble: {
            color: "#FFC000",
            minSize: '10%',
            maxSize: '100%',
            zMin: 0,
            zMax: 20,
            layoutAlgorithm: {
                gravitationalConstant: 0.02,
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

const PipelineTags = ({ pipelines, ...props }) => {

    const [options, setOptions] = useState(defaultOptions);
    const [isDrawn, setIsDrawn] = useState(false);

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
    };

    const constructData = () => {

        const chartData = {
            pipelines: {}
        };

        pipelines.elements.forEach(pipeline => {

            if (!pipeline.tags.domain)
                return;

            if (!Array.isArray(pipeline.tags.domain)) {
                addOrIncreaseDatapoint(chartData.pipelines, pipeline.tags.domain);
                return;
            }
            const tagsArr = pipeline.tags.domain;

            tagsArr.forEach(tag => {
                addOrIncreaseDatapoint(chartData.pipelines, tag);
            })

        })

        updateChart(chartData);

    };

    const addOrIncreaseDatapoint = (data, point) => {
        if (!Object.keys(data).includes(point)) {
            data[point] = 1;
        }
        else {
            data[point] += 1;
        }
    }

    if (pipelines && !isDrawn) {
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

PipelineTags.propTypes = {

};

PipelineTags.defaultProps = {

};

export default PipelineTags;
