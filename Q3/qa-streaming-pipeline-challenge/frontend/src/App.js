import './App.css';
import axios from "axios";
import React, { Component } from 'react';
import Regression from './Regression.js';
import ClassificationChart from './Classification.js';

class App extends Component {

  constructor() {
    super();
    this.state = {classification_data: [], regression_data:[], r2:0}
  };

  runScript = () => {
  axios.get("/api/v1/run_script")
    .then((response) => {
    // handle success
    console.log(response);
    let data = response.data[0]
    let new_data_point = { x:data.num_records_processed, y:response.data[0].accuracy}
    this.setState({classification_data: this.state.classification_data.concat(new_data_point)})
    let regression_data_size = data.indep.length
    for (let i = 0; i < regression_data_size; i+=100){
      let new_data_point = { x:data.indep[i], y:data.depend[i]}
      this.setState({regression_data: this.state.regression_data.concat(new_data_point)})
      }
    this.setState({r2: data.r2})
    })
    .catch(function (error) {
      // handle error
    console.log(error);
    })
}

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div className='myRow'>
            <ClassificationChart dataObject={this.state.classification_data}/>
            <Regression dataObject={this.state.regression_data} r2={this.state.r2}/>
          </div>
          <button color="primary" onClick={this.runScript}>
            Update
          </button>
        </header>
      </div>
    );
  }
}

export default App;
