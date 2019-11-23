import React, { Component } from "react";

class Home extends Component {
    render() {

        //Style 
        const buttonStyle = {

            marginRight: 0,
            marginLeft: 0,
            marginTop: 0,
            paddingTop: 0,
            paddingBottom: 0,
            

            color: "Orange",
            fontWeight: "Bold",
            

            backgroundColor: 'rgba(52, 52, 52, 0)',
            fontSize: '64px',
            borderRadius: 10,
            borderWidth: 0,
            borderColor: '#000'

        }
        return (
            <div
                style={{


                    display: "flex",
                    justifyContent: "right",
                    alignItems: "right",
                    position: 'absolute',
                    top: '2.25vh',
                    right: '7vw',

                }}
            >
                <button

                    style={buttonStyle}
                    onClick={this.shoot}>
                    ⌂
                    </button>

            </div>
        );
    }
}

export default Home;