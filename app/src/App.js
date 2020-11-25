import React, { useState } from 'react';
import LeaderboardPage from './pages/Leaderboard/LeaderboardPage';
import HomePage from './pages/Home/HomePage';
import PuzzlePage from './pages/Puzzle/PuzzlePage';
import LoginPage from './pages/Login/LoginPage';
import AccessTokenContext from './context/AccessTokenContext';

import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


function App(props) {
  const [accessToken, setAccessToken] = useState('');
  const isLoggedIn = accessToken !== '';

  return (
    <AccessTokenContext.Provider value={{ accessToken, setAccessToken, isLoggedIn }}>
      <Router>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
        <div data-testid="app">
          <Switch>
            {isLoggedIn && (
              <>
                <Route path="/mypuzzles">
                  <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                  <LeaderboardPage />
                </Route>
                <Route path="/puzzle/:puzzleId">
                  <PuzzlePage />
                </Route>
              </>
            )}
            <Route path="/"><LoginPage /></Route>
          </Switch>
        </div>
      </Router>
    </AccessTokenContext.Provider>
  );
}

export default App;
