import React from 'react';
import GoogleMapComponent from './GoogleMapComponent'
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';

export default class MapContainer extends React.Component {
  constructor() {
    super();
    this.state = { address: '' };
  }

  render() {
    console.log('rendering map')
    return (
      <div className="MapContainer">
        <GooglePlacesAutocomplete onSelect= {
            ({ description }) => {
            this.setState({ address: description })
            console.log(description)
          }}
        />
        <GoogleMapComponent coords={this.props.location.coords}/>
      </div>
    );
  }
}
