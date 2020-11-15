import React from 'react'

export default class Home extends React.Component {
    render() {
        const {isAuthenticated, getAccessToken} = this.props.auth
        console.log(isAuthenticated())
        console.log(getAccessToken())
        return (
            <div className="Home" data-testid="home">
                {isAuthenticated() &&  getAccessToken()}
            </div>
            );
    }
}
