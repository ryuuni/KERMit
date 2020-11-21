import './App.css';
import React, { useState, useEffect } from 'react';
import LeaderboardPage from './pages/Leaderboard/LeaderboardPage';
import HomePage from './pages/Home/HomePage';
import PuzzlePage from './pages/Puzzle/PuzzlePage';
import LoginPage from './pages/Login/LoginPage';
import AccessTokenContext from './context/AccessTokenContext';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";


function App(props) {
  const [accessToken, setAccessToken] = useState('');
  const isLoggedIn = accessToken !== '';
  const history = useHistory();

  useEffect(() => {
    if (!accessToken) {
      history.push('/login');
    }
  }, [accessToken, history]);

  return (
    <AccessTokenContext.Provider value={{ accessToken, setAccessToken, isLoggedIn }}>
      <Router>
        <div data-testid="app">
          {isLoggedIn ? (
            <Switch>
              <Route path="/mypuzzles">
                <HomePage />
              </Route>
              <Route path="/leaderboard-view">
                <LeaderboardPage />
              </Route>
              <Route path="/puzzle/:puzzleId">
                <PuzzlePage />
              </Route>
              <Route path="/">
                <HomePage />
              </Route>
            </Switch>
          ) : <Route><LoginPage path="/login" /></Route>}
        </div>
      </Router>
    </AccessTokenContext.Provider>
  );
}

export default App;
