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
function getStartingPoint(props) {
  if (props.line[0]) return { lat: props.line[0].lat, lng: props.line[0].lng };
  else return { lat: 0, lng: 1 };
}
const MyMapComponent = withScriptjs(withGoogleMap((props) =>
  <GoogleMap
    defaultZoom={15}
    defaultCenter={getStartingPoint(props)}
    initialCenter={getStartingPoint(props)}
    defaultOptions={{
      disableDefaultUI: true, // disable default map UI
      draggable: true, // make map draggable
      keyboardShortcuts: false, // disable keyboard shortcuts
      scaleControl: true, // allow scale controle
      scrollwheel: true, // allow scroll wheel
      styles: styles // change default map styles
    }}>
    <Polyline
      path={props.line}
      options={{
        strokeWeight:'3',
        strokeOpacity:'.9',
        strokeColor:'orange'
      }}
    />
    <Polyline
      path={props.line}
      options={{
        strokeWeight:'15',
        strokeOpacity:'.2',
        strokeColor:'orange'
      }}
    />
    <Marker
      icon={{url:'https://img.icons8.com/offices/30/000000/pin.png'}}
      position={getStartingPoint(props)}
    />
    <Marker
      icon={{url:'https://img.icons8.com/office/30/000000/walking.png'}}
      position={getStartingPoint(props)}
    />
  </GoogleMap>
))

export default class MapContainer extends React.Component {
  render() {
    return <div style={ style }><MyMapComponent
      line={ this.props.polyline }
      googleMapURL={ string }
      loadingElement={<div style={{ height: `100%` }} />}
      containerElement={<div style={style} />}
      mapElement={<div style={style} />}
/></div>
  }
}
