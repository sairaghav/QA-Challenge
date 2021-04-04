import React, { Component } from 'react';
import CanvasJSReact from './canvasjs.react';
var CanvasJSChart = CanvasJSReact.CanvasJSChart;

class ClassificationChart extends Component {

	render() {
		const options = {
			theme: "light2",
			animationEnabled: true,
			exportEnabled: true,
			title: {
				text: "Accuracy of the Classification Model"
			},
            axisX: {
				title: "Number of Records Processed"
			},
			axisY: {
				title: "Accuracy (%)"
			},
			data: [{
					type: "line",
					indexLabelFontSize: 16,
					dataPoints: this.props.dataObject
				}]
		}

		return (
		<div>
			<h1>Classification Model</h1>
			<CanvasJSChart options = {options}/>
		</div>
		);
	}
}

export default ClassificationChart;