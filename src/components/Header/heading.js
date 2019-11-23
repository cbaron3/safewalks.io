import React from "react";
import { geolocated } from "react-geolocated";

//This class/element serves as the heading of the app, displaying the logo

class Heading extends React.Component {

    render() {
        return (
            <div
                style={{
                    color: "orange",
                    display: "flex",
                    justifyContent: "left",
                    alignItems: "left",
                    fontSize: "150%"
                }}
            >
                <h1>safeWalks</h1>

            </div>
        )
    }
}

export default Heading;