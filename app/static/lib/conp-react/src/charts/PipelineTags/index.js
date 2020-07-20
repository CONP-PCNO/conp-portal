import React, { useState } from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";
require('highcharts/highcharts-more.js')(Highcharts);
import HighchartsReact from 'highcharts-react-official'
import { pipe } from "ramda";

const defaultOptions = {

    chart: {
        type: 'packedbubble',
        //styledMode: true,
        backgroundColor: '#FFF',
        height: '40%'
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Most Popular Pipeline Tags'
    },

    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value}'
    },

    plotOptions: {
        packedbubble: {
            color: Highcharts.getOptions().colors[1],
            minSize: '20%',
            maxSize: '100%',
            zMin: 0,
            zMax: 30,
            layoutAlgorithm: {
                gravitationalConstant: 0.1,
                splitSeries: true,
                seriesInteraction: false,
                dragBetweenSeries: true,
                parentNodeLimit: true
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

            tagsArr.map(tag => {
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
