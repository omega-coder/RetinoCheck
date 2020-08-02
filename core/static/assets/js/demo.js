"use strict";
// Cicle Chart
Circles.create({
  id: "task-complete",
  radius: 50,
  value: 80,
  maxValue: 100,
  width: 5,
  text: function (value) {
    return value + "%";
  },
  colors: ["#36a3f7", "#fff"],
  duration: 400,
  wrpClass: "circles-wrp",
  textClass: "circles-text",
  styleWrapper: true,
  styleText: true,
});

//Notify
$.notify(
  {
    icon: "fas fa-check-circle",
    title: "Connected",
    message: "You are now connected as fy_cherief@esi.dz",
  },
  {
    type: "success",
    placement: {
      from: "bottom",
      align: "right",
    },
    time: 1000,
  }
);

// JQVmap
$("#map-example").vectorMap({
  map: "world_en",
  backgroundColor: "transparent",
  borderColor: "#fff",
  borderWidth: 2,
  color: "#e4e4e4",
  enableZoom: true,
  hoverColor: "#35cd3a",
  hoverOpacity: null,
  normalizeFunction: "linear",
  scaleColors: ["#b6d6ff", "#005ace"],
  selectedColor: "#35cd3a",
  selectedRegions: ["ID", "RU", "US", "AU", "CN", "BR"],
  showTooltip: true,
  onRegionClick: function (element, code, region) {
    return false;
  },
});

//Chart

var ctx = document.getElementById("statisticsChart").getContext("2d");

var statisticsChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "100",
      "200",
      "300",
      "400",
      "500",
      "600",
      "700",
      "800",
      "900",
      "1000",
      "1100",
      "1200",
    ],
    datasets: [
      {
        label: "ResNet50",
        borderColor: "#f3545d",
        pointBackgroundColor: "rgba(243, 84, 93, 0.6)",
        pointRadius: 0,
        backgroundColor: "rgba(243, 84, 93, 0.4)",
        legendColor: "#f3545d",
        fill: true,
        borderWidth: 2,
        data: [40, 30, 40, 50, 55, 60, 67, 70, 71, 74, 77, 82],
      },
      {
        label: "ResNet + InceptionV3",
        borderColor: "#fdaf4b",
        pointBackgroundColor: "rgba(253, 175, 75, 0.6)",
        pointRadius: 0,
        backgroundColor: "rgba(253, 175, 75, 0.4)",
        legendColor: "#fdaf4b",
        fill: true,
        borderWidth: 2,
        data: [40, 30, 40, 50, 55, 60, 67, 70, 71, 74, 77, 95],
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    legend: {
      display: true,
    },
    tooltips: {
      bodySpacing: 4,
      mode: "nearest",
      intersect: 0,
      position: "nearest",
      xPadding: 10,
      yPadding: 10,
      caretPadding: 10,
    },
    layout: {
      padding: { left: 5, right: 5, top: 15, bottom: 15 },
    },
    scales: {
      yAxes: [
        {
          ticks: {
            fontStyle: "500",
            beginAtZero: false,
            maxTicksLimit: 5,
            padding: 10,
          },
          gridLines: {
            drawTicks: false,
            display: false,
          },
        },
      ],
      xAxes: [
        {
          gridLines: {
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: 10,
            fontStyle: "500",
          },
        },
      ],
    },
    legendCallback: function (chart) {
      var text = [];
      text.push('<ul class="' + chart.id + '-legend html-legend">');
      for (var i = 0; i < chart.data.datasets.length; i++) {
        text.push(
          '<li><span style="background-color:' +
            chart.data.datasets[i].legendColor +
            '"></span>'
        );
        if (chart.data.datasets[i].label) {
          text.push(chart.data.datasets[i].label);
        }
        text.push("</li>");
      }
      text.push("</ul>");
      return text.join("");
    },
  },
});

var myLegendContainer = document.getElementById("myChartLegend");

// generate HTML legend
myLegendContainer.innerHTML = statisticsChart.generateLegend();

// bind onClick event to all LI-tags of the legend
var legendItems = myLegendContainer.getElementsByTagName("li");
for (var i = 0; i < legendItems.length; i += 1) {
  legendItems[i].addEventListener("click", legendClickCallback, false);
}

var dailySalesChart = document
  .getElementById("dailySalesChart")
  .getContext("2d");

var myDailySalesChart = new Chart(dailySalesChart, {
  type: "line",
  data: {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
    ],
    datasets: [
      {
        label: "Sales Analytics",
        fill: !0,
        backgroundColor: "rgba(255,255,255,0.2)",
        borderColor: "#fff",
        borderCapStyle: "butt",
        borderDash: [],
        borderDashOffset: 0,
        pointBorderColor: "#fff",
        pointBackgroundColor: "#fff",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "#fff",
        pointHoverBorderWidth: 1,
        pointRadius: 1,
        pointHitRadius: 5,
        data: [30, 40, 55, 60, 66, 70, 78, 83, 93],
      },
    ],
  },
  options: {
    maintainAspectRatio: !1,
    legend: {
      display: !1,
    },
    animation: {
      easing: "easeInOutBack",
    },
    scales: {
      yAxes: [
        {
          display: !1,
          ticks: {
            fontColor: "rgba(0,0,0,0.5)",
            fontStyle: "bold",
            beginAtZero: !0,
            maxTicksLimit: 10,
            padding: 0,
          },
          gridLines: {
            drawTicks: !1,
            display: !1,
          },
        },
      ],
      xAxes: [
        {
          display: !1,
          gridLines: {
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: -20,
            fontColor: "rgba(255,255,255,0.2)",
            fontStyle: "bold",
          },
        },
      ],
    },
  },
});

$("#activeUsersChart").sparkline(
  [112, 109, 120, 107, 110, 85, 87, 90, 102, 109, 120, 99, 110, 85, 87, 94],
  {
    type: "bar",
    height: "100",
    barWidth: 9,
    barSpacing: 10,
    barColor: "rgba(255,255,255,.3)",
  }
);

var topProductsChart = document
  .getElementById("topProductsChart")
  .getContext("2d");

var myTopProductsChart = new Chart(topProductsChart, {
  type: "line",
  data: {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "January",
      "February",
      "March",
      "April",
    ],
    datasets: [
      {
        label: "Sales Analytics",
        fill: !0,
        backgroundColor: "rgba(53, 205, 58, 0.2)",
        borderColor: "#35cd3a",
        borderCapStyle: "butt",
        borderDash: [],
        borderDashOffset: 0,
        pointBorderColor: "#35cd3a",
        pointBackgroundColor: "#35cd3a",
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "#35cd3a",
        pointHoverBorderColor: "#35cd3a",
        pointHoverBorderWidth: 1,
        pointRadius: 1,
        pointHitRadius: 5,
        data: [
          20,
          10,
          18,
          14,
          32,
          18,
          15,
          22,
          8,
          6,
          17,
          12,
          17,
          18,
          14,
          25,
          18,
          12,
          19,
          21,
          16,
          14,
          24,
          21,
          13,
          15,
          27,
          29,
          21,
          11,
          14,
          19,
          21,
          17,
        ],
      },
    ],
  },
  options: {
    maintainAspectRatio: !1,
    legend: {
      display: !1,
    },
    animation: {
      easing: "easeInOutBack",
    },
    scales: {
      yAxes: [
        {
          display: !1,
          ticks: {
            fontColor: "rgba(0,0,0,0.5)",
            fontStyle: "bold",
            beginAtZero: !0,
            maxTicksLimit: 10,
            padding: 0,
          },
          gridLines: {
            drawTicks: !1,
            display: !1,
          },
        },
      ],
      xAxes: [
        {
          display: !1,
          gridLines: {
            zeroLineColor: "transparent",
          },
          ticks: {
            padding: -20,
            fontColor: "rgba(255,255,255,0.2)",
            fontStyle: "bold",
          },
        },
      ],
    },
  },
});
