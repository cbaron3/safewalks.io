import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render(){
    return (
        <div class="form">
            <form action="http://0.0.0.0:5000/api/safe-place" method="get">
            </form>
        </div>
    );
}
}

export default App;
