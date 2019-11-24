import React from 'react';

export default class MapContainer extends React.Component {
  render() {
    return (
      <div className="LoadingComponent"
      style={{
          color: "white",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          paddingTop: '20vh',
          right: '7vw',
          paddingLeft: '5vw',
          fontSize: "12vh",
          fontWeight: "lighter",
      }}
    >loading...</div> )
  }
}
