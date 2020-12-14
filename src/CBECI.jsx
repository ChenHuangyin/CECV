
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import * as Highcharts from 'highcharts/highstock';

class CBECI extends Component {
	
	componentDidMount() {
		this.createChart();
	}

	componentDidUpdate() {
    	this.createChart();
  	}

	createChart() {
		let estimatedData = [];
		estimatedData = this.props.estimatedData.map(obj => {
			const date = obj['Date'].split("/");
			const dateInSeconds = new Date(`20${date[2]}`, +date[1] - 1, date[0]).getTime();
			return [dateInSeconds, obj['Estimated Consumption']];
		}).reverse();

		let minimumData = [];
		minimumData = this.props.minimumData.map(obj => {
			const date = obj['Date'].split("/");
			const dateInSeconds = new Date(`20${date[2]}`, +date[1] - 1, date[0]).getTime();
			return [dateInSeconds, obj['Minimum Consumption']];
        }).reverse();
        
        let maximumData = [];
		maximumData = this.props.maximumData.map(obj => {
			const date = obj['Date'].split("/");
			const dateInSeconds = new Date(`20${date[2]}`, +date[1] - 1, date[0]).getTime();
			return [dateInSeconds, obj['Maximum Consumption']];
		}).reverse();

		Highcharts.stockChart('chart', {
			rangeSelector: {
				selected: 5
			},

			title: {
				text: this.props.title
			},
			yAxis: {
                title: {
                    text: 'Twh per Year'
				},
				tickInterval: 10
			},
			plotOptions: {
				series: {
					showInNavigator: true,
					split: true
				}
			},	
			series: [{
					name: 'Estimated Consumption',
					data: estimatedData,
					tooltip: {
						valueDecimals: 5
					}
				},
				{
					name: 'Minimum Consumption',
					data: minimumData,
					tooltip: {
						valueDecimals: 5
					}
                }, 
                {
                    name: 'Maximum Consumption',
                    data: maximumData,
                    tooltip: {
						valueDecimals: 5
					}
                }
            ],
			credits: {
				enabled: false
			}
    	});
	}

	render() {
		return (
			<div id='chart'>Highstock</div>
		);
	}
}

CBECI.propTypes = {
	data: PropTypes.array,
  	title: PropTypes.string
};

export default CBECI;