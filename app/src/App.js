import React, { useState } from 'react';
import LeaderboardPage from './pages/Leaderboard/LeaderboardPage';
import HomePage from './pages/Home/HomePage';
import PuzzlePage from './pages/Puzzle/PuzzlePage';
import LoginPage from './pages/Login/LoginPage';
import CurrentUserContext from './context/CurrentUserContext';

import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


function App(props) {
  const [accessToken, setAccessToken] = useState('');
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const isLoggedIn = accessToken !== '';

  return (
    <CurrentUserContext.Provider value={{ accessToken, setAccessToken, userName, setUserName, userEmail, setUserEmail, isLoggedIn }}>
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
    </CurrentUserContext.Provider>
  );
}

export default App;
