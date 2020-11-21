import './App.css';
import GoogleBtn from './GoogleBtn';
import React, { useState } from 'react';
import Leaderboard from './LeaderboardPageComponents/Leaderboard';
import Puzzles from './HomePageComponents/Puzzles';
import Puzzle from './PuzzlePageComponents/PuzzlePage';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";


function App(props) {
  const [accessToken, setAccessToken] = useState('');
  const loggedIn = accessToken !== '';

  return (
    <Router>
      <div className="App" data-testid="app">
        {loggedIn && (
          <div className="nav-item">
            <Link to="/mypuzzles">My Puzzles</Link>
          </div>
        )}
        {loggedIn && (
          <div className="nav-item">
            <Link to="/leaderboard-view">Leaderboard</Link>
          </div>
        )}
        <div className="login-btn" data-testid="login-btn">
          <GoogleBtn onAccessTokenChanged={token => setAccessToken(token)}/>
        </div>
        <div className="page-content">
          {loggedIn ? (
            <Switch>
              <Route path="/mypuzzles">
                <Puzzles accessToken={accessToken}/>
              </Route>
              <Route path="/leaderboard-view">
                <Leaderboard accessToken={accessToken}/>
              </Route>
              <Route path="/puzzle/:puzzleId">
                <Puzzle accessToken={accessToken} />
              </Route>
              <Route path="/">
                <Puzzles accessToken={accessToken}/>
              </Route>
            </Switch>
          ):(
            <div>
              <p className="japanese-name">一緒に数独</p>
              <h1>Isshoni Sudoku</h1>
              <div className="login-btn" data-testid="login-btn">
                <GoogleBtn onAccessTokenChanged={token => setAccessToken(token)}/>
              </div>
            </div>
          )}
        </div>
      </div>
    </Router>
  );

}

export default App;
