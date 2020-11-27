import React, { Component } from "react";
import PropTypes from "prop-types";
import * as Highcharts from "highcharts/highstock";

class ECI extends Component {
  componentDidMount() {
    this.createChart();
  }

  componentDidUpdate() {
    this.createChart();
  }

  createChart() {
    let estimatedData = [];
    estimatedData = this.props.estimatedData
      .map((obj) => {
        const date = obj["Date"].split("/");
        const dateInSeconds = new Date(
          `20${date[2]}`,
          +date[1] - 1,
          date[0]
        ).getTime();
        return [dateInSeconds, obj["Estimated TWh per Year"]];
      })
      .reverse();

    let minimumData = [];
    minimumData = this.props.minimumData
      .map((obj) => {
        const date = obj["Date"].split("/");
        const dateInSeconds = new Date(
          `20${date[2]}`,
          +date[1] - 1,
          date[0]
        ).getTime();
        return [dateInSeconds, obj["Minimum TWh per Year"]];
      })
      .reverse();

    Highcharts.stockChart("chart", {
      rangeSelector: {
        selected: 5,
      },

      title: {
        text: this.props.title,
      },
      plotOptions: {
        series: {
          showInNavigator: true,
          split: true,
        },
      },
      series: [
        {
          name: "Estimated TWh per Year",
          data: estimatedData,
          tooltip: {
            valueDecimals: 5,
          },
        },
        {
          name: "Minimum TWh per Year",
          data: minimumData,
          tooltip: {
            valueDecimals: 5,
          },
        },
      ],
      credits: {
        enabled: false,
      },
    });
  }

  render() {
    return <div id="chart">Highstock</div>;
  }
}

ECI.propTypes = {
  data: PropTypes.array,
  title: PropTypes.string,
};

export default ECI;
