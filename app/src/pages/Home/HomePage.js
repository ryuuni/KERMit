import './HomePage.css';
import React, { useState, useContext, useEffect, useCallback } from 'react';
import { Redirect } from "react-router-dom";
import CreatePuzzleModalContent from '../../components/CreatePuzzleModalContent/CreatePuzzleModalContent';
import HidePuzzleModal from '../../components/HidePuzzleModal/HidePuzzleModal';
import PuzzleCard from '../../components/PuzzleCard/PuzzleCard';
import CurrentUserContext from '../../context/CurrentUserContext';
import PageTemplate from '../Template/PageTemplate';
import Modal from '@material-ui/core/Modal';
import Endpoint from '../../utils/Endpoint';

const HomePage = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [puzzles, setPuzzles] = useState([]);
  const [redirect, setRedirect] = useState(null);
  const [hidePuzzleId, setHidePuzzleId] = useState(-1);
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [hideModalOpen, setHideModalOpen] = useState(false);
  const { accessToken } = useContext(CurrentUserContext);

  const redirectToPuzzle = useCallback(puzzleId => {
    setRedirect(`/puzzle/${puzzleId}`);
  }, []);

  const createGame = useCallback(({difficulty, additionalPlayers}) => {
    if (difficulty >= 0.1 && difficulty <= 0.99) {
      const size = 3;
      const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}` },
        body: JSON.stringify({
          'additional_players': additionalPlayers,
          'difficulty': difficulty,
          'size': size,
        }),
      };
      const url = Endpoint.createPuzzle({difficulty, size, additionalPlayers});
      fetch(url, requestOptions).then(res => res.json()).then(data => {
        redirectToPuzzle(data.puzzle_id);
      });
    }
  }, [accessToken, redirectToPuzzle]);

  const updatePuzzles = useCallback((accessToken, setPuzzles) => {
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
  }, []);

  const hidePuzzle = useCallback(() => {
    if (hidePuzzleId !== -1) {
      const requestOptions = {
        method: 'POST',
        headers: { Authorization: `Bearer ${accessToken}` },
        body: JSON.stringify({
          'hidden': true,
        }),
      };
      const url = Endpoint.hidePuzzle({hidePuzzleId});
      fetch(url, requestOptions).then(res => res.json()).then(data => {
        setHideModalOpen(false);
        updatePuzzles(accessToken, setPuzzles);
      });
    }
  }, [accessToken, hidePuzzleId, setPuzzles, updatePuzzles]);

  useEffect(() => {
    updatePuzzles(accessToken, setPuzzles);
  }, [accessToken, setPuzzles, updatePuzzles]);

  if (redirect) {
    return <Redirect to={redirect} />
  }

  return (
    <PageTemplate>
      <div className="homepage">
        <button className="new-game-btn" onClick={() => setCreateModalOpen(true)}>
          Start new puzzle
        </button>
        <Modal
          open={createModalOpen}
          onClose={() => setCreateModalOpen(false)}
        >
          <CreatePuzzleModalContent createGame={createGame} />
        </Modal>
        <Modal
          open={hideModalOpen}
          onClose={() => setHideModalOpen(false)}
        >
          <HidePuzzleModal puzzleId={hidePuzzleId} setHideModalStatus={setHideModalOpen} hidePuzzle={hidePuzzle}/>
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
              hideModalOpen={hideModalOpen}
              setHideModalStatus={setHideModalOpen}
              setHidePuzzleId={setHidePuzzleId}
            />
          ))}
        </div>
      </div>
    </PageTemplate>
  );
}

export default HomePage;
