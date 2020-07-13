import React from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";

const ModalityDatasets = ({ datasets, pipelines, ...props }) => {

    const drawChart = (data) => {

        console.log(JSON.stringify(data));

        const xAxis = [];

        Highcharts.chart('dashboard-chart', {

            chart: {
                type: 'column',
                styledMode: true,
                backgroundColor: '#FFF'
            },
            credits: {
                enabled: false
            },

            title: {
                text: 'Most Popular Dataset Types'
            },

            yAxis: [{
                title: {
                    text: '',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                allowDecimals: false,
            }],

            /*
            xAxis: {
                categories: xAxis
            }, */

            plotOptions: {
                column: {
                    borderRadius: 5
                }
            },

            series: [{
                name: 'Datasets',
                data: Object.values(data.datasets),
                yAxis: 0
            },
            {
                name: 'Pipelines',
                data: Object.values(data.pipelines),
                yAxis: 0
            }]

        })
    };

    const contructData = () => {

        const chartData = {
            datasets: {},
            pipelines: {}
        };

        datasets.elements.forEach(dataset => {

            console.log(dataset.modalities);

            if (!dataset.modalities)
                return;

            const modalitiesArr = dataset.modalities.split(", ");

            modalitiesArr.map(modality => {
                console.log(modality);
                addOrIncreaseDatapoint(chartData.datasets, modality);
            })
        })

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

ModalityDatasets.propTypes = {

};

ModalityDatasets.defaultProps = {

};

export default ModalityDatasets;
