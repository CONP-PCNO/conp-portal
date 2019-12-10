import React from "react";
import PropTypes from "prop-types";
import Highcharts from "highcharts";

const DashboardChart = props => {
  const { ...data } = props;

  Highcharts.chart('dashboard-chart-container', {

    chart: {
        type: 'column',
        styledMode: true,
        backgroundColor: '#FFF'
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Number of Datasets and Pipelines in 2019'
    },

    yAxis: [{
        className: 'highcharts-color-0',
        title: {
            text: 'Number of Pipelines'
        }
    }, {
        className: 'highcharts-color-1',
        opposite: true,
        title: {
            text: 'Number of Datasets'
        }
    }],

    xAxis: {
    categories: ["January'19", "February'19", "March'19","April'19"]
    },

    plotOptions: {
        column: {
            borderRadius: 5
        }
    },



    series: [{
        name: 'CONP Datasets',
        data: [0, 0, 0, 6]
    }, {
        name: 'CONP Pipelines',
        data: [0, 0, 0, 8],
        yAxis: 1
    }]

});

  return (
    <div id="dashboard-chart"/>
  );
};

DashboardChart.propTypes = {
  
};

DashboardChart.defaultProps = {
  
};

export default DashboardChart;
