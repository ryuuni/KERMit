import {createContext} from 'react'

const CurrentUserContext = createContext({
  accessToken: '',
  userName: '',
  userEmail: '',
  isLoggedIn: false,
  setAccessToken: () => {},
  setUserName: () => {}, 
  setUserEmail: () => {},
});

export default CurrentUserContext;