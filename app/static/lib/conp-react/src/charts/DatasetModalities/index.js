import React, { useState } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'
require('highcharts/highcharts-more.js')(Highcharts);

const defaultOptions = {

    chart: {
        type: 'packedbubble',
        backgroundColor: '#FFF',
        height: '50%',
        spacing: [0, 0, 0, 0],
        margin: [0, 0, 0, 0]
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Dataset Modalities by Keyword'
    },

    tooltip: {
        useHTML: true,
        pointFormat: '<b>{point.name}:</b> {point.value}'
    },

    plotOptions: {
        packedbubble: {
            color: Highcharts.getOptions().colors[0],
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
            name: 'Dataset Modalities',
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

            modalitiesArr.forEach(modality => {
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
