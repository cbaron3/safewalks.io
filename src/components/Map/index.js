import React from 'react';
import { API_KEY } from '../../../src/secrets.js'
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';
import { geolocated } from "react-geolocated";

class MapContainer extends React.Component {
  render() {

    //Style 
    const style = {
      width: '90vw',
      height: '80vh',
      'marginLeft': 'auto',
      'marginRight': 'auto'
    }

    console.log(`Available: ${this.props.isGeolocationAvailable}`)
    console.log(`Enabled: ${this.props.isGeolocationEnabled}`)

    return (

      <Map
      style = { style }
      google={this.props.google}
      zoom={14}
      initialCenter={{
            lat: 43.0096,
            lng: -81.2737
      }}
      >

        <Marker onClick={this.onMarkerClick}
                name={'Current location'} />

        <InfoWindow onClose={this.onInfoWindowClose}>
            <div>
              <h1>Hi</h1>
            </div>
        </InfoWindow>
      </Map>
    );
  }
}

const LoadingContainer = (props) => (
  <div>Fancy loading container!</div>
)

export default GoogleApiWrapper({
  apiKey: API_KEY,
  LoadingContainer: LoadingContainer
})(MapContainer)
