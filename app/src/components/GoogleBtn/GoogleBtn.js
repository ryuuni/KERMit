import React, { useCallback, useContext } from 'react'
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import register from '../../utils/ApiClient.js';
import AccessTokenContext from '../../context/AccessTokenContext';
import { useHistory } from 'react-router-dom';

const CLIENT_ID = '950548208840-dq7hp4pt98dlq05idlh3cn5juiqjqlpf.apps.googleusercontent.com';

/**
 * Class skeleton adapted from: https://zoejoyuliao.medium.com
 * /add-google-sign-in-and-sign-out-to-your-react-app-and-
 * get-the-accesstoken-2ee16bfd8297
 */
const GoogleBtn = () => {
  const { isLoggedIn, setAccessToken } = useContext(AccessTokenContext);
  const history = useHistory();

  const login = useCallback(response => {
    if (response.accessToken) {
      setAccessToken(response.accessToken);
      register(response.accessToken);
    }
  }, [setAccessToken]);
  const logout = useCallback(() => {
    setAccessToken('');
    history.push('/');
  }, [setAccessToken, history]);
  const handleLoginFailure = useCallback(response => {
    alert('Failed to log in');
  }, []);
  const handleLogoutFailure = useCallback(response => {
    alert('Failed to log out')
  }, []);

  return (
    <div>
      { isLoggedIn ?
        <GoogleLogout
          clientId={CLIENT_ID}
          buttonText='Logout'
          onLogoutSuccess={logout}
          onFailure={handleLogoutFailure}
        >
        </GoogleLogout> : <GoogleLogin
          clientId={CLIENT_ID}
          buttonText='Login'
          onSuccess={login}
          onFailure={handleLoginFailure}
          cookiePolicy={'single_host_origin'}
          responseType='code,token'
          isSignedIn={true}
        />
      }
    </div>
  );
};

export default GoogleBtn;