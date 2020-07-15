import React, { useState } from "react";
import PropTypes from "prop-types";
import { useDebounce } from "react-use";
import * as qs from "query-string";

import Highcharts from "highcharts";
require('highcharts/highcharts-more.js')(Highcharts);
import HighchartsReact from 'highcharts-react-official'

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
        text: 'Dataset Modalities'
    },

    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value}'
    },

    plotOptions: {
        packedbubble: {
            color: Highcharts.getOptions().colors[0],
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

    series: []

};

const DatasetModalities = ({ datasets, pipelines, ...props }) => {

    const [options, setOptions] = useState(defaultOptions);
    const [isDrawn, setIsDrawn] = useState(false);

    const updateChart = (data) => {

        const datasetData = Object.keys(data.datasets).map(d => {
            return {
                name: d,
                value: data.datasets[d]
            };
        });

        const series = [{
            name: 'Datasets',
            data: datasetData
        }];

        setOptions(prevOptions => ({
            ...prevOptions,
            series: series,
        }));
    };

    const constructData = () => {

        const chartData = {
            datasets: {}
        };

        datasets.elements.forEach(dataset => {

            if (!dataset.modalities)
                return;

            const modalitiesArr = dataset.modalities.split(", ");

            modalitiesArr.map(modality => {
                addOrIncreaseDatapoint(chartData.datasets, modality);
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

    if (datasets && pipelines && !isDrawn) {
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

DatasetModalities.propTypes = {

};

DatasetModalities.defaultProps = {

};

export default DatasetModalities;
