import { useParams } from "react-router-dom";
import { useState, useEffect, useContext, useRef, useCallback } from "react"
import SudokuBoard from '../../components/SudokuBoard/SudokuBoard';
import Chat from '../../components/Chat/Chat';
import CurrentUserContext from '../../context/CurrentUserContext';
import PageTemplate from '../Template/PageTemplate';
import socketIOClient from "socket.io-client";
import './PuzzlePage.css'

async function getPuzzle({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`http://localhost:5000/puzzles/${puzzleId}`, requestOptions)
  const json = await response.json();
  onSuccess(json);
}

const PuzzlePage = () => {
  const { puzzleId } = useParams();
  const [pieces, setPieces] = useState(null);
  const [solved, setSolved] = useState(false);
  const [isMultiplayerGame, setIsMultiplayerGame] = useState(false);
  const [messages, setMessages] = useState([]);
  const { accessToken } = useContext(CurrentUserContext);
  const socket = useRef(null); 

  const updatePuzzle = useCallback(({pieces, completed, players}) => {
    setPieces(
      pieces.sort((pieceA, pieceB) =>
        (pieceA.y_coordinate * 10 + pieceA.x_coordinate) - (pieceB.y_coordinate * 10 + pieceB.x_coordinate)
    ));
    setSolved(completed);
    if (players !== undefined) {
      setIsMultiplayerGame(players.length > 1);
    }
  }, []);

  const addMessage = useCallback((data) => {
    setMessages(oldMessages => [...oldMessages, data]);
  }, []);

  useEffect(() => {  
    socket.current = socketIOClient("ws://127.0.0.1:5000/", {query: {auth: accessToken}, transports: ['websocket']});

    const currSocket = socket.current;

    if (currSocket.disconnected) {
      currSocket.connect({query: {auth: accessToken}});
    }
    currSocket.emit('join', {puzzle_id: puzzleId, token: accessToken});

    currSocket.on("player_joined", data => {
      console.log('player joined:');
      console.log(data);
    });

    currSocket.on("puzzle_update", ({pieces, completed}) => {
      console.log(pieces);
      console.log(completed);
      updatePuzzle({pieces, completed})
    });

    currSocket.on("message_update", (data) => {
      console.log('got message:');
      console.log(data);
      addMessage(data);
    })

    getPuzzle({
      accessToken,
      puzzleId,
      onSuccess: updatePuzzle,
    });

    return () => {
      currSocket.emit('leave', {puzzle_id: puzzleId});
      currSocket.disconnect();
    };
  }, [accessToken, puzzleId, socket, updatePuzzle, addMessage]);

  return (
    <PageTemplate>
      <div className={isMultiplayerGame ? 'puzzle-page' : null}>
        <div className={isMultiplayerGame ? 'puzzle-board' : null}>
          <SudokuBoard
            data-testid='sudoku-board'
            gridState={pieces}
            puzzleId={puzzleId}
            solved={solved}
            ref={socket}
          />
        </div>
        {isMultiplayerGame && <div className="chat"><Chat messages={messages} puzzleId={puzzleId} ref={socket}/></div> }
      </div>
    </PageTemplate>
  );
}

export default PuzzlePage;