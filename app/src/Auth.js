// import auth0 from 'auth0-js';
// import history from './history';

export default class Auth {
  constructor() {
    localStorage.setItem('isLoggedIn', false)
    localStorage.setItem('accessToken', '')
  }

  // checks if the user is authenticated
  isAuthenticated = () => {
    return localStorage.getItem('isLoggedIn')
  }

  getAccessToken = () => {
    return localStorage.getItem('accessToken')
  }

  storeSuccessfulLogin = (accessToken) => {
    localStorage.setItem('isLoggedIn', true)
    localStorage.setItem('accessToken', accessToken)
  }

  storeSuccessfulLogout = () => {
    localStorage.setItem('isLoggedIn', false)
    localStorage.setItem('accessToken', '')
  }
}