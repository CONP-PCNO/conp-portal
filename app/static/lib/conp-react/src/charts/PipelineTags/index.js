import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";
require('highcharts/highcharts-more.js')(Highcharts);

const PipelineTags = ({ datasets, pipelines, ...props }) => {

    const drawChart = (data) => {

        console.log(JSON.stringify(data));

        const pipelineData = Object.keys(data.pipelines).map(p => {
            return {
                name: p,
                value: data.pipelines[p]
            };
        });

        console.log(JSON.stringify(pipelineData));

        Highcharts.chart('dashboard-chart', {

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
                text: 'Pipeline Tags'
            },

            tooltip: {
                useHTML: true,
                pointFormat: '<b>{point.name}:</b> {point.value}'
            },

            plotOptions: {
                packedbubble: {
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
                            value: 2
                        },
                        style: {
                            color: 'black',
                            textOutline: 'none',
                            fontWeight: 'normal'
                        }
                    }
                }
            },

            series: [{
                name: 'Pipelines',
                data: pipelineData
            }]

        })
    };

    const contructData = () => {

        const chartData = {
            pipelines: {}
        };

        pipelines.elements.forEach(pipeline => {

            console.log(pipeline.tags.domain);

            if (!pipeline.tags.domain)
                return;

            if(!Array.isArray(pipeline.tags.domain)) {
                addOrIncreaseDatapoint(chartData.pipelines, pipeline.tags.domain);
                return;
            }
            const tagsArr = pipeline.tags.domain;

            tagsArr.map(tag => {
                console.log(tag);
                addOrIncreaseDatapoint(chartData.pipelines, tag);
            })

        })

        drawChart(chartData);

    };

    const addOrIncreaseDatapoint = (data, point) => {
        if (!Object.keys(data).includes(point)) {
            console.log(point + " does not exist");
            data[point] = 1;
        }
        else {
            data[point] += 1;
            console.log(point + " is now " + data[point]);
        }
    }

    useDebounce(() => void contructData(), 300);

    return (
        <div id="dashboard-chart" />
    );
};

PipelineTags.propTypes = {

};

PipelineTags.defaultProps = {

};

export default PipelineTags;
