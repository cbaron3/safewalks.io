import React from 'react';
import { withScriptjs, withGoogleMap, GoogleMap, Marker, Polyline } from "react-google-maps"
import { API_KEY } from '../../src/secrets.js'
import decodePolyline from 'decode-google-map-polyline'
const styles = require('./googleMapStyles.json')

const string = `https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${API_KEY}`
const polyline = decodePolyline("{ineGfhaoNFpAvKe@tDQzKc@zGa@bAMx@[v@g@p@s@t@qAPk@hAl@RBPCjAi@fDoAfCnM")
const style = {
  
  width: '90vw',
  height: '75vh',
  borderBottomLeftRadius: '15px',
  borderBottomRightRadius: '15px',
  marginLeft: 'auto',
  marginRight: 'auto'

}
const MyMapComponent = withScriptjs(withGoogleMap((props) =>
  <GoogleMap
    defaultZoom={15}
    defaultCenter={{ lat: (polyline[0].lat+polyline[polyline.length-1].lat)/2, lng: (polyline[0].lng+polyline[polyline.length-1].lng)/2 }}
    initialCenter={{
        lat: polyline[0].lat,
        lng: polyline[0].lng
    }}
    defaultOptions={{

      disableDefaultUI: true, // disable default map UI
      draggable: true, // make map draggable
      keyboardShortcuts: false, // disable keyboard shortcuts
      scaleControl: true, // allow scale controle
      scrollwheel: true, // allow scroll wheel
      styles: styles // change default map styles

    }}>
    <Polyline
      path={polyline}
      options={{
        strokeWeight:'3',
        strokeOpacity:'.9',
        strokeColor:'orange'
      }}
    />
    <Polyline
      path={polyline}
      options={{
        strokeWeight:'15',
        strokeOpacity:'.2',
        strokeColor:'orange'
      }}
    />
  </GoogleMap>
))

export default class MapContainer extends React.Component {
  render() {
    return <div style={style} ><MyMapComponent
      isMarkerShown
      googleMapURL={ string }
      loadingElement={<div style={{ height: `100%` }} />}
      containerElement={<div style={style} />}
      mapElement={<div style={ style } />}
/></div>
  }
}
