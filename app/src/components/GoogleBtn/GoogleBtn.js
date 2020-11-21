import React, { Component } from 'react'
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import register from '../../utils/ApiClient.js';

const CLIENT_ID = '950548208840-dq7hp4pt98dlq05idlh3cn5juiqjqlpf.apps.googleusercontent.com';

/**
 * Class skeleton taken from: https://zoejoyuliao.medium.com
 * /add-google-sign-in-and-sign-out-to-your-react-app-and-
 * get-the-accesstoken-2ee16bfd8297
 */
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

  login(response) {
    if (response.accessToken) {
      this.setState(state => ({
        isLoggedIn: true,
        accessToken: response.accessToken
      }));
    }
    this.props.onAccessTokenChanged(response.accessToken)
    console.log('response: ')
    register(this.state.accessToken);
  }

  logout(response) {
    this.setState(state => ({
      isLoggedIn: false,
      accessToken: ''
    }));
    this.props.onAccessTokenChanged(this.state.accessToken)
  }

  handleLoginFailure(response) {
    alert('Failed to log in')
  }

  handleLogoutFailure(response) {
    alert('Failed to log out')
  }

  render() {
    return (
      <div>
        { this.state.isLoggedIn ?
          <GoogleLogout
            clientId={CLIENT_ID}
            buttonText='Logout'
            onLogoutSuccess={this.logout}
            onFailure={this.handleLogoutFailure}
          >
          </GoogleLogout> : <GoogleLogin
            clientId={CLIENT_ID}
            buttonText='Login'
            onSuccess={this.login}
            onFailure={this.handleLoginFailure}
            cookiePolicy={'single_host_origin'}
            responseType='code,token'
          />
        }
      </div>
    )
  }
}

export default GoogleBtn;