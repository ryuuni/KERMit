import React, { Component } from 'react'
import { GoogleLogin, GoogleLogout } from 'react-google-login';

const CLIENT_ID = '950548208840-dq7hp4pt98dlq05idlh3cn5juiqjqlpf.apps.googleusercontent.com';

class GoogleBtn extends Component {
   constructor(props) {
    super(props);

    this.state = {
      isLoggedIn: false,
      accessToken: ''
    };

    this.login = this.login.bind(this);
    this.handleLoginFailure = this.handleLoginFailure.bind(this);
    this.logout = this.logout.bind(this);
    this.handleLogoutFailure = this.handleLogoutFailure.bind(this);
  }

  login (response) {
    if(response.accessToken){
      this.setState(state => ({
        isLoggedIn: true,
        accessToken: response.accessToken
      }));
    }
    this.props.onAccessTokenChanged(response.accessToken)
    console.log('response: ')
    const requestOptions = {
      method: 'POST',
      headers: { Authorization: `Bearer ${this.state.accessToken}` },
    };
    fetch('/register', requestOptions).then(res => res.json()).then(data => {
      console.log(data)
    });
  }

  logout (response) {
    this.setState(state => ({
      isLoggedIn: false,
      accessToken: ''
    }));
    this.props.onAccessTokenChanged(this.state.accessToken)
  }

  handleLoginFailure (response) {
    alert('Failed to log in')
  }

  handleLogoutFailure (response) {
    alert('Failed to log out')
  }

  render() {
    return (
    <div>
      { this.state.isLoggedIn ?
        <GoogleLogout
          clientId={ CLIENT_ID }
          buttonText='Logout'
          onLogoutSuccess={ this.logout }
          onFailure={ this.handleLogoutFailure }
        >
        </GoogleLogout>: <GoogleLogin
          clientId={ CLIENT_ID }
          buttonText='Login'
          onSuccess={ this.login }
          onFailure={ this.handleLoginFailure }
          cookiePolicy={ 'single_host_origin' }
          responseType='code,token'
        />
      }
    </div>
    )
  }
}

export default GoogleBtn;