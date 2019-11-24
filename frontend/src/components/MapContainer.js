import React from 'react';
import MapComponent from './MapComponent'
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import axios from 'axios'

const style = {
  width: '90vw',
  borderRadius: '10px',
  marginLeft: 'auto',
  marginRight: 'auto'
}

export default class MapContainer extends React.Component {
  constructor() {
    super();
    this.state = { address: '' };
  }

  render() {
    return (
      <div className="MapContainer" style={ style }>
        <GooglePlacesAutocomplete onSelect= {
            ({ description }) => {
            this.setState({ address: description })
            console.log(description)
          }}
        />
        <MapComponent />
      </div>
    );
  }
}
