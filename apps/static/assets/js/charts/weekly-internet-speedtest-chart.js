<!-- javascript init -->
// General configuration for the charts with Line gradientStroke
gradientChartOptionsConfiguration = {
    maintainAspectRatio: false,
    legend: {
        display: true,
        position: 'top'
    },
    tooltips: {
        backgroundColor: '#fff',
        titleFontColor: '#333',
        bodyFontColor: '#666',
        bodySpacing: 4,
        xPadding: 12,
        mode: "nearest",
        intersect: 0,
        position: "nearest"
    },
    responsive: true,
    scales: {
        yAxes: [{
            barPercentage: 1.6,
            gridLines: {
                drawBorder: false,
                color: 'rgba(29,140,248,0.0)',
                zeroLineColor: "transparent",
            },
            ticks: {
                suggestedMin: 30,
                suggestedMax: 60,
                padding: 20,
                fontColor: "#9a9a9a"
            }
        }],

        xAxes: [{
            barPercentage: 1.6,
            gridLines: {
                drawBorder: false,
                color: 'rgba(220,53,69,0.1)',
                zeroLineColor: "transparent",
            },
            ticks: {
                padding: 20,
                fontColor: "#9a9a9a"
            }
        }]
    }
};

var weeklyInternetSpeedtestChart = document.getElementById("weekly-internet-speedtest-chart").getContext("2d");

var gradientStroke = weeklyInternetSpeedtestChart.createLinearGradient(0, 230, 0, 50);

gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

// Ajax callback function uses getLatestWeekSpeedtestAjax to retreive data from a view/api then draw it
ajaxCallback()

function getLatestWeekSpeedtestAjax(callback) {
    $.ajax({
        url: window.location.href +
            'latest_week_internet_speedtests/',
        type: "GET",
        dataType: "json",
        success: (data) => {
            callback(data);
        },
        error: (error) => {
            console.log(error);
        }

    });

};

function ajaxCallback() {
    getLatestWeekSpeedtestAjax(function (response) {
        //processing the data
        console.log(response);
        var labels = [];
        var downloadData = [];
        var uploadData = [];

        for (var item in response) {
            labels.push(response[item].created)
            downloadData.push(response[item].download)
            uploadData.push(response[item].upload)
        }
        // drawChart uses the labes, (datasets) to draw—assign data to chart HTML element
        drawChart(labels, downloadData, uploadData);

    });
};

function drawChart(labels, downloadData, uploadData) {
    // Sets chart datasets and configurations
    var chartData = {
        // TODO: Fix lables adjustments, the date is  too long it makes the chart look bad
        labels: labels,
        datasets: [
            {
                label: "Download Speed",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: downloadData,
            },
            {
                label: "Upload Speed",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d0c548',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d0c548',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d0c548',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: uploadData,
            }
        ]

    };

    var myChart = new Chart(weeklyInternetSpeedtestChart, {
        type: 'line',
        data: chartData,
        options: gradientChartOptionsConfiguration
    });

};
