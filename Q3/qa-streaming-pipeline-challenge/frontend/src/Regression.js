import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;
 
class Regression extends Component {
	render() {
		const options = {
			theme: "light2",
			animationEnabled: true,
			exportEnabled: true,
			title: {
				text: "Promoted Vs Network Ability"
			},
			axisX: {
				title: "Promoted - R^2 Value is: " +  parseFloat(this.props.r2.toFixed(2)),
				minimum: -0.2,
				maximum: 1.2
			},
			axisY: {
				title: "Network Ability"
			},
			data: [{
					type: "scatter",
					indexLabelFontSize: 16,
					dataPoints: this.props.dataObject
				}]
		}
		
		return (
		<div>
			<h1>Regression Model</h1>
			<CanvasJSChart options = {options}/>
		</div>
		);
	}
}

export default Regression;