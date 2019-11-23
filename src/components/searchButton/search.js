import React, { Component } from "react";

class Search extends Component {
    render() {

        //Style 
        const buttonStyle = {

            marginRight: 0,
            marginLeft: 0,
            marginTop: 0,
            paddingTop: 0,
            paddingBottom: 0,
            backgroundColor: 'rgba(52, 52, 52, 0)',
            fontSize: '40px',
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
                    top: '4vh',
                    right: '18vw',

                }}
            >
                <button

                    style={buttonStyle}
                    onClick={this.shoot}>
                    🔍
                    </button>

            </div>
        );
    }
}

export default Search;