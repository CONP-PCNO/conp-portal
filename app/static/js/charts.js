
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
        text: 'Number of Datasets and Pipelines'
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
    categories: ["April'19", "May'19", "June'19","July'19"]
    },

    plotOptions: {
        column: {
            borderRadius: 5
        }
    },



    series: [{
        name: 'Datasets',
        data: [5, 10, 15, 25]
    }, {
        name: 'Pipelines',
        data: [10, 20, 30, 50],
        yAxis: 1
    }]

});