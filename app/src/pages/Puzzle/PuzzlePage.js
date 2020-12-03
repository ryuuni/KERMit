import { useParams } from "react-router-dom";
import { useState, useEffect, useContext, useRef, useCallback } from "react"
import SudokuBoard from '../../components/SudokuBoard/SudokuBoard';
import Chat from '../../components/Chat/Chat';
import CurrentUserContext from '../../context/CurrentUserContext';
import PageTemplate from '../Template/PageTemplate';
import socketIOClient from "socket.io-client";
import Endpoint from '../../utils/Endpoint';
import './PuzzlePage.css'

async function getPuzzle({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(Endpoint.getPuzzle({puzzleId}), requestOptions);
  const json = await response.json();
  onSuccess(json);
}

const PuzzlePage = () => {
  const { puzzleId } = useParams();
  const [pieces, setPieces] = useState(null);
  const [solved, setSolved] = useState(false);
  const [messages, setMessages] = useState([]);
  const [playersLockingCells, setPlayersLockingCells] = useState({});
  const [players, setPlayers] = useState([]);
  const isMultiplayerGame = players.length > 1;
  const { accessToken } = useContext(CurrentUserContext);
  const socket = useRef(null); 

  const updatePuzzle = useCallback(({pieces, completed, players}) => {
    setPieces(
      pieces.sort((pieceA, pieceB) =>
        (pieceA.y_coordinate * 10 + pieceA.x_coordinate) - (pieceB.y_coordinate * 10 + pieceB.x_coordinate)
    ));
    setSolved(completed);
    console.log('PLAYERS:');
    console.log(players);
    if (players !== undefined) {
      setPlayers(players);
    }
  }, []);

  const addMessage = useCallback((data) => {
    setMessages(oldMessages => [...oldMessages, data]);
  }, []);
  
  useEffect(() => {  
    getPuzzle({
      accessToken,
      puzzleId,
      onSuccess: updatePuzzle,
    });
  }, []);

  useEffect(() => {
    const currSocket = socketIOClient("ws://127.0.0.1:5000/", {query: {auth: accessToken}, transports: ['websocket']});
    socket.current = currSocket;

    if (currSocket.disconnected) {
      currSocket.connect({query: {auth: accessToken}});
    }
    currSocket.emit('join', {puzzle_id: puzzleId, token: accessToken});
    
    return () => {
      currSocket.emit('leave', {puzzle_id: puzzleId});
      currSocket.disconnect();
    };
  }, []);

  useEffect(() => {  
    socket.current.on("puzzle_update", ({pieces, completed}) => {
      console.log(pieces);
      console.log(completed);
      updatePuzzle({pieces, completed})
    });

    return () => {
      socket.current.removeAllListeners('puzzle_update');
    };
  }, [socket, updatePuzzle]);

  useEffect(() => {  
    socket.current.on("message_update", (data) => {
      console.log('got message:');
      console.log(data);
      addMessage(data);
    });

    return () => {
      socket.current.removeAllListeners('message_update');
    };
  }, [socket, addMessage]);

  useEffect(() => {  
    socket.current.on('lock_update_remove', ({x_coordinate: x, y_coordinate: y}) => {
      const newPlayersLockingCells = {...playersLockingCells};
      delete newPlayersLockingCells[coordsToString(x, y)];
      setPlayersLockingCells(newPlayersLockingCells);
    });

    return () => {
      socket.current.removeAllListeners('lock_update_remove');
    };
  }, [socket, playersLockingCells]);

  useEffect(() => {  
    socket.current.on('lock_update_add', ({x_coordinate: x, y_coordinate: y, player}) => {
      setPlayersLockingCells({
        ...playersLockingCells, 
        [coordsToString(x, y)]: {player, index: players.findIndex(p => p.id === player.id)}
      });
    });

    return () => {
      socket.current.removeAllListeners('lock_update_add');
    };
  }, [socket, players, playersLockingCells]);

  useEffect(() => {  
    socket.current.on("player_joined", data => {
      console.log('player joined:');
      console.log(data);
    });

    return () => {
      socket.current.removeAllListeners('player_joined');
    };
  }, [socket]);

  return (
    <PageTemplate>
      <div className={isMultiplayerGame ? 'puzzle-page' : null}>
        <div className={isMultiplayerGame ? 'puzzle-board' : null}>
          <SudokuBoard
            data-testid='sudoku-board'
            players={players}
            playersLockingCells={playersLockingCells}
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

function coordsToString(x, y) {
  return `${x},${y}`;
}

export default PuzzlePage;