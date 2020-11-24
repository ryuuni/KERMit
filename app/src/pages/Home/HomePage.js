import './HomePage.css';
import React, { useState, useContext, useEffect, useCallback } from 'react';
import { Redirect } from "react-router-dom";
import CreatePuzzleModalContent from '../../components/CreatePuzzleModalContent/CreatePuzzleModalContent';
import PuzzleCard from '../../components/PuzzleCard/PuzzleCard';
import AccessTokenContext from '../../context/AccessTokenContext';
import PageTemplate from '../Template/PageTemplate';
import Modal from '@material-ui/core/Modal';
import Endpoint from '../../utils/Endpoint';

const HomePage = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [puzzles, setPuzzles] = useState([]);
  const [redirect, setRedirect] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const { accessToken } = useContext(AccessTokenContext);

  const redirectToPuzzle = useCallback(puzzleId => {
    setRedirect(`/puzzle/${puzzleId}`);
  }, []);

  const createGame = useCallback((difficulty) => {
    if (difficulty >= 0.1 && difficulty <= 0.99) {
      const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}` },
      };
      const url = Endpoint.createPuzzle({difficulty});
      fetch(url, requestOptions).then(res => res.json()).then(data => {
        redirectToPuzzle(data.puzzle_id);
      });
    }
  }, [accessToken, redirectToPuzzle]);

  useEffect(() => {
    const requestOptions = {
      method: 'GET',
      headers: { Authorization: `Bearer ${accessToken}` },
    };
    fetch(Endpoint.getPuzzles(), requestOptions).then(res => res.json()).then(data => {
      setIsLoaded(true);
      if (data.puzzles !== undefined) {
        setPuzzles(data.puzzles);
      }
    });
  }, [accessToken, setPuzzles]);

  if (redirect) {
    return <Redirect to={redirect} />
  }

  return (
    <PageTemplate>
      <div className="homepage">
        <button className="new-game-btn" onClick={() => setModalOpen(true)}>
          Start new puzzle
        </button>
        <Modal
          open={modalOpen}
          onClose={() => setModalOpen(false)}
        >
          <CreatePuzzleModalContent createGame={createGame} />
        </Modal>
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
