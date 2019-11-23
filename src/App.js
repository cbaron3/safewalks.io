import React from 'react';
import logo from './logo.svg';
import './App.css';
import LocationContainer from './components/Location/index'
import MapContainer from './components/Map/index'
import Heading from './components/Header/heading'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Heading/>
        <MapContainer/>
      </header>
    </div>
  );
}


export default App;
