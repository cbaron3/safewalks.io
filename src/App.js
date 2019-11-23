import React from 'react';
import logo from './logo.svg';
import './App.css';
import LocationContainer from './components/Location/index'
import MapContainer from './components/Map/index'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <LocationContainer/>
        <MapContainer/>
      </header>
    </div>
  );
}

export default App;
