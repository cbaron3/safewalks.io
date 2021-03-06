import React, { Component } from 'react';
import MapContainer from './MapContainer'
import LoadingComponent from './LoadingComponent'
import Heading from './Header/heading'
import Home from './takeMeHomeButton/takeMeHome'

export default class AppContainer extends Component {

  constructor() {
    super();
    this.state = { }
  }

  componentDidMount() {
    navigator.geolocation.getCurrentPosition(position => {
      console.log('got position')
      this.setState({
        allowed_location: true,
        location: position
      });
    },
    error => {
      console.log('error getting position')
      this.setState({
        allowed_location: false
      });
    }, { enableHighAccuracy: true });
  }

  render() {
    var visible;
    if(this.state.allowed_location === false) {
      visible =       <div className="LoadingComponent"
      style={{
          color: "white",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          paddingTop: '20vh',
          right: '7vw',
          paddingLeft: '5vw',
          fontSize: "6vh",
          fontWeight: "lighter"
      }}>Please enable location services</div>
    }
    else {
      if(this.state.allowed_location === undefined) visible = <LoadingComponent />
      else visible = <MapContainer coords={this.state.location.coords}/>
    }
    return (
      <div className="AppContainer">
        <Heading />
        <Home />
        { visible }
      </div>
    );
  }
}
