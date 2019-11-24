import React from 'react';
import { withScriptjs, withGoogleMap, GoogleMap, Marker, Polyline } from "react-google-maps"
import { API_KEY } from '../../src/secrets.js'
import decodePolyline from 'decode-google-map-polyline'
const styles = require('./googleMapStyles.json')

const string = `https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${API_KEY}`
const style = {
  width: '90vw',
  height: '75vh',
  borderRadius: '10px',
  'marginLeft': 'auto',
  'marginRight': 'auto',
}
function renderLines(lines, max) {
  let renders = [];
  if(lines !== undefined) {
    lines.forEach(line => {
      const polyline = decodePolyline(line.polyline);
      if(line.polyline === max) {
        renders.push(
          <Polyline
            path={polyline}
            options={{
              strokeWeight:'3',
              strokeOpacity:'.9',
              strokeColor:'orange'
            }}
          />
        )
        renders.push(
          <Polyline
            path={polyline}
            options={{
              strokeWeight:'15',
              strokeOpacity:'.2',
              strokeColor:'orange'
            }}
          />
        )
      }
      else {
        renders.push(
          <Polyline
            path={polyline}
            options={{
              strokeWeight:'3',
              strokeOpacity:'.5',
              strokeColor:'yellow'
            }}
          />
        )
        renders.push(
          <Polyline
            path={polyline}
            options={{
              strokeWeight:'15',
              strokeOpacity:'.1',
              strokeColor:'yellow'
            }}
          />
        )
      }
    })
  }
  return renders;
}
function getStartingPoint(props) {
  if (props.line) {
    const line = decodePolyline(props.line);
    return { lat: props.line[0].lat, lng: props.line[0].lng };
  }
  else return { lat: 43.0071039, lng: -81.283014 };
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
    { renderLines(props.lines, props.line) }
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
      line={ this.props.max_polyline }
      lines={ this.props.polylines }
      googleMapURL={ string }
      loadingElement={<div style={{ height: `100%` }} />}
      containerElement={<div style={style} />}
      mapElement={<div style={{ height: `100%` }} />}
/></div>
  }
}
