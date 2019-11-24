import React from 'react';
import MapComponent from './MapComponent'
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import axios from 'axios'
import encodeurl from 'encodeurl'
import decodePolyline from 'decode-google-map-polyline'
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
    this.state = { polyline: '' };
  }

  render() {
    return (
      <div className="MapContainer" style={ style }>
        <GooglePlacesAutocomplete onSelect= {
            ({ description }) => {
            this.setState({ address: description })
            var url = encodeurl(BACKEND_URL + `/api/path?from=${this.props.coords.latitude},${this.props.coords.longitude}&to=${description}`);
            axios.get(url)
            .then(response => {
              var line;
              var indexOfMaxLine = -1;
              var index = 0;
              var maxSafety = 0;
              response.data.forEach(x => {
                if(x.rating > maxSafety) {
                  maxSafety = x.rating;
                  indexOfMaxLine = index;
                }
                index++;
              });
              line = response.data[indexOfMaxLine].polyline
              this.setState({
                polylines: response.data,
                max_polyline: line,
                lights: response.data[indexOfMaxLine].in_range_lights,
                all_lights: response.data
              });
            })
            .catch(error => {
              console.log(error)
            });
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
        <MapComponent polylines = { this.state.polylines } max_polyline={ this.state.max_polyline } location={ this.state.coords } lights={ this.state.lights } all_lights={ this.state.all_lights }/>
      </div>
    );
  }
}
