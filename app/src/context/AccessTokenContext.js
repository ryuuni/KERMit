import {createContext} from 'react'

const AccessTokenContext = createContext({
  accessToken: '',
  isLoggedIn: false,
  setAccessToken: () => {},
});

export default AccessTokenContext;