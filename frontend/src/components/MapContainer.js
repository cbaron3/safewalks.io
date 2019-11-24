import React from 'react';
import MapComponent from './MapComponent'
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import axios from 'axios'
import encodeurl from 'encodeurl'
import { BACKEND_URL } from '../../src/secrets.js'

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
            console.log(this.props);
            var url = encodeurl(BACKEND_URL + `/api/path?from=${this.props.location.coords.latitude},${this.props.location.coords.longitude}&to=${description}'`);
            axios.get(url)
            .then(response => {
              console.log(response)
            })
            .catch(error => {
              console.log(error)
            });
          }}
        />
        <MapComponent />
      </div>
    );
  }
}
