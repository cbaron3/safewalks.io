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
                    top: '2.25vh',
                    right: '7vw',
                    paddingLeft: '7vw',

                    fontSize: "3vh"
                }}
            >
                <h1>safeWalks</h1>

            </div>
        )
    }
}

export default Heading;
