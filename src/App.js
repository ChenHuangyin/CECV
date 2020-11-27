
import React, { Component } from 'react';
import { BECIEstimated, BECIMinimum } from './data/BECI';
import { EECIEstimated, EECIMinimum } from './data/EECI';
import ECI from './ECI';
import * as _ from 'lodash';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selected: 1,
      estimatedData: _.cloneDeep(BECIEstimated),
      minimumData: _.cloneDeep(BECIMinimum),
      title: 'Bitcoin Energy Consumption Index'
    };
  }

  BECISelected = () => {
    this.setState({
      selected: 1,
      estimatedData: _.cloneDeep(BECIEstimated),
      minimumData: _.cloneDeep(BECIMinimum),
      title: 'Bitcoin Energy Consumption Index'
    });
  }

  EECISelected = () => {
    this.setState({
      selected: 2,
      estimatedData: _.cloneDeep(EECIEstimated),
      minimumData: _.cloneDeep(EECIMinimum),
      title: 'Ethereum Energy Consumption Index'
    });
  }

  render() {
    let content;
    content = <ECI estimatedData={this.state.estimatedData} minimumData={this.state.minimumData} title={this.state.title} />;
    
    return (
      <div className="App">
        <div className="App-header">
          <h2>Cryptocurrency Energy Consumption Visualization</h2>
        </div>
        <div className="container">
          <div className="nav">
            <button type='button' className={"btn btn-highchart " + (this.state.selected === 1 ? 'active' : '')} onClick={this.BECISelected}>BECI</button>
            <button type='button' className={"btn btn-highchart " + (this.state.selected === 2 ? 'active' : '')} onClick={this.EECISelected}>EECI</button>
          </div>
          {content}
        </div>
      </div>
    );
  }
}

export default App;
