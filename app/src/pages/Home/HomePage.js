import './HomePage.css';
import React, { useState, useContext, useEffect, useCallback } from 'react';
import { Redirect } from "react-router-dom";
import PuzzleCard from '../../components/PuzzleCard/PuzzleCard';
import AccessTokenContext from '../../context/AccessTokenContext';
import PageTemplate from '../Template/PageTemplate';
import {socket} from "../../utils/Socket.js";

const HomePage = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [puzzles, setPuzzles] = useState([]);
  const [redirect, setRedirect] = useState(null);
  const { accessToken } = useContext(AccessTokenContext);

  const redirectToPuzzle = useCallback(puzzleId => {
    setRedirect(`/puzzle/${puzzleId}`);
  }, []);

  const createGame = useCallback(() => {
    const requestOptions = {
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken}` },
    };
    fetch('http://localhost:5000/puzzles?difficulty=0.1&size=3', requestOptions).then(res => res.json()).then(data => {
      redirectToPuzzle(data.puzzle_id);
    });
  }, [accessToken, redirectToPuzzle]);

  useEffect(() => {
    const requestOptions = {
      method: 'GET',
      headers: { Authorization: `Bearer ${accessToken}` },
    };
    fetch('http://localhost:5000/puzzles', requestOptions).then(res => res.json()).then(data => {
      setIsLoaded(true);
      setPuzzles(data.puzzles);
    });
  }, [accessToken, setPuzzles]);

  if (redirect) {
    return <Redirect to={redirect} />
  }

  return (
    <PageTemplate>
      <div className="homepage">
        <button className="new-game-btn" onClick={createGame}>
          Start new puzzle
        </button>
        {puzzles.length === 0 && isLoaded
          && (<div className="empty-message">
            You do not currently have any puzzles. Start a new one using the button above!
          </div>)}
        <div className="puzzle-cards" data-testid="puzzle-cards">
          {puzzles.map(puzzle => (
            <PuzzleCard
              puzzle={puzzle}
              key={puzzle.puzzle_id}
              onClick={redirectToPuzzle}
            />
          ))}
        </div>
      </div>
    </PageTemplate>
  );
}

export default HomePage;
