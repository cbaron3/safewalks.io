import React from 'react';
import { withScriptjs, withGoogleMap, GoogleMap, Marker, Polyline, Circle } from "react-google-maps"
import { DrawingManager } from "react-google-maps/lib/components/drawing/DrawingManager"
import { API_KEY } from '../../src/secrets.js'
import decodePolyline from 'decode-google-map-polyline'
const styles = require('./googleMapStyles.json')

const string = `https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=${API_KEY}`
const style = {

  width: '90vw',
  height: '75vh',
  borderBottomLeftRadius: '15px',
  borderBottomRightRadius: '15px',
  marginLeft: 'auto',
  marginRight: 'auto'
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
              strokeOpacity:'.2',
              strokeColor:'orange'
            }}
          />
        )
        renders.push(
          <Polyline
            path={polyline}
            options={{
              strokeWeight:'10',
              strokeOpacity:'.1',
              strokeColor:'orange'
            }}
          />
        )
      }
    })
  }
  return renders;
}

function renderLights(lights) {
  let renders = [];
  if(lights !== undefined) {
    lights.forEach(light => {
        renders.push(
          <Marker
            icon={{url:'https://i.imgur.com/Zmc99Hv.png'}}
            position={{ lat: light.latitude, lng: light.longitude }}
          />
        )
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
    { renderLights(props.lights) }
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
      lights={ this.props.lights }
      googleMapURL={ string }
      loadingElement={<div style={{ height: `100%` }} />}
      containerElement={<div style={style} />}
      mapElement={<div style={style} />}
/></div>
  }
}
