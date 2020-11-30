import {createContext} from 'react'

const AccessTokenContext = createContext({
  accessToken: '',
  userName: '',
  userEmail: '',
  isLoggedIn: false,
  setAccessToken: () => {},
  setUserName: () => {}, 
  setUserEMail: () => {},
});

export default AccessTokenContext;