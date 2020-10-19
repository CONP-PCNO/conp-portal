import React, { useState } from "react";

import Highcharts from "highcharts";
import HighchartsReact from 'highcharts-react-official'
require('highcharts/highcharts-more.js')(Highcharts);

const getCircularReplacer = () => {
    const seen = new WeakSet();
    return (key, value) => {
      if (typeof value === "object" && value !== null) {
        if (seen.has(value)) {
          return;
        }
        seen.add(value);
      }
      return value;
    };
  };
  
const defaultOptions = {

    chart: {
        type: 'packedbubble',
        backgroundColor: '#FFF',
        height: '100%',
        spacing: [0, 0, 0, 0],
        margin: [0, 0, 0, 0],
        colors: ["#EA2627", "#A5A5A5", "#FFC000", "#207EA0", "#898989", "#5E5E5E"]
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
        series:{
            allowPointSelect: true,
            point:{
                events:{
                  select: function(e){
                    console.log(e)
                    // eslint-disable-next-line no-restricted-globals
                    location.assign(`/search?modalities=${e.target.name}`)
                  }
                }
              }
          },

        packedbubble: {
            color: "#EA2627",
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
            },
            allowPointSelect: true
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
