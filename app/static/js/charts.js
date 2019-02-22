
Highcharts.chart('chart', {

    chart: {
        type: 'column',
        styledMode: true,
        backgroundColor: '#FFF'
    },
    credits: {
        enabled: false
    },

    title: {
        text: 'Datasets and Pipelines'
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

    plotOptions: {
        column: {
            borderRadius: 5
        }
    },

    series: [{
        data: [1, 3, 2, 4]
    }, {
        data: [324, 124, 547, 221],
        yAxis: 1
    }]

});