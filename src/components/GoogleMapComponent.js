import React from 'react';
import { API_KEY } from '../../src/secrets.js'
import LoadingComponent from './LoadingComponent'
import decodePolyline from 'decode-google-map-polyline'
import { Map, Marker, GoogleApiWrapper, Polyline } from 'google-maps-react';

class MapContainer extends React.Component {

  render() {
    const polyline = decodePolyline("{ineGfhaoNFpAvKe@tDQzKc@zGa@bAMx@[v@g@p@s@t@qAPk@hAl@RBPCjAi@fDoAnChN")
    return (
      <Map
        google={this.props.google}
        zoom={14}
        initialCenter={{
              lat: polyline[0].lat,
              lng: polyline[0].lng
        }}>

        <Marker
          title={'Start of trip'}
          position={{lat: polyline[0].lat, lng: polyline[0].lng}} />

          <Marker
            title={'End of trip'}
            position={{lat: polyline[polyline.length-1].lat, lng: polyline[polyline.length-1].lng}} />

        <Polyline
        fillColor="#0000FF"
        fillOpacity={0.35}
        path={polyline}
        strokeColor="#0000FF"
        strokeOpacity={0.8}
        strokeWeight={2}
      />

      </Map>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: API_KEY,
  LoadingContainer: LoadingComponent
})(MapContainer)
