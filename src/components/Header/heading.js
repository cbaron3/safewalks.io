import React from "react";

//This class/element serves as the heading of the app, displaying the logo

class Heading extends React.Component {

    render() {
        return (
            <div
                style={{
                    color: "orange",
                    display: "flex",
                    justifyContent: "left",
                    alignItems: "center",
                    paddingTop: '2vh',
                    right: '7vw',
                    paddingLeft: '5vw',

                    fontSize: "8vh",
                    fontWeight: "lighter",
                }}
            >
                safeWalks

            </div>
        )
    }
}

export default Heading;
