import React, { Component } from 'react';
import './App.css';
import CreatePizza from './components/CreatePizza';

class App extends Component{
    render(){
      return (
        <div className="App">
          <header className="App-header">
            <CreatePizza/>
          </header>
        </div>
  );
 }
}

export default App;
