import React from 'react';
import GoogleMapComponent from './GoogleMapComponent'
import MapComponent from './MapComponent'
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';

const style = {

  width: '90vw',
  borderRadius: '15px',
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
      <div className="MapContainer" style={style}>
        <GooglePlacesAutocomplete onSelect={
          ({ description }) => {
            this.setState({ address: description })
            console.log(description)
          }}

          placeholder='Where to?'

          inputStyle={{
            background: '#262F3D',
            color: 'orange',
            fontSize: "3vh",
            fontWeight: "lighter",
          }}

          suggestionsStyles={{
            container: {
              color: 'orange',
            },
            suggestion: {
              background: '#262F3D',
              fontSize: "2vh",
              fontWeight: "lighter"
            },
          }}
        />
        <MapComponent />
      </div>
    );
  }
}
