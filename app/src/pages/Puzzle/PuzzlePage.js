import { useParams } from "react-router-dom";
import { useState, useEffect, useContext, useRef } from "react"
import SudokuBoard from '../../components/SudokuBoard/SudokuBoard';
import AccessTokenContext from '../../context/AccessTokenContext';
import PageTemplate from '../Template/PageTemplate';
// import { getPuzzleResponse } from '../data/get_puzzle_response'
// import { getSolutionResponse, getSolvedSolutionResponse } from '../data/get_solution_response'
import io from "socket.io-client";

const ONE_SECOND_IN_MILLIS = 1000;

async function getPuzzle({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`http://localhost:5000/puzzles/${puzzleId}`, requestOptions)
  // const response = await Promise.resolve(getPuzzleResponse());
  const json = await response.json();
  onSuccess(json);
}

const PuzzlePage = () => {
  const { puzzleId } = useParams();
  const [pieces, setPieces] = useState(null);
  const [solved, setSolved] = useState(false);
  const { accessToken } = useContext(AccessTokenContext);
  const socket = useRef(null); 

  useEffect(() => {
    const getPuzzleSubscription = setInterval(() => getPuzzle({
      accessToken,
      puzzleId,
      onSuccess: json => {setPieces(
        json.pieces.sort((pieceA, pieceB) =>
          (pieceA.y_coordinate * 10 + pieceA.x_coordinate) - (pieceB.y_coordinate * 10 + pieceB.x_coordinate)
        ))
        setSolved(json.completed)
      },
    }), ONE_SECOND_IN_MILLIS);

    socket.current = io("ws://127.0.0.1:5000/", {transports: ['websocket']});
    let currSocket = socket.current;
    if (currSocket.disconnected) {
      currSocket.connect();
    }
    currSocket.emit('join', {puzzle_id: puzzleId});
    currSocket.on("player_joined", data => {
      console.log('player joined:');
      console.log(data);
    });
    currSocket.on("puzzle_update", data => {
      console.log('puzzle updated:');
      console.log(data);
    });

    return () => {
      currSocket.emit('leave', {puzzle_id: puzzleId});
      currSocket.disconnect();
      clearInterval(getPuzzleSubscription);
    };
  }, [accessToken, puzzleId, socket]);

  return (
    <PageTemplate>
      <SudokuBoard
        data-testid='sudoku-board'
        gridState={pieces}
        puzzleId={puzzleId}
        solved={solved}
        socket={socket.current}
      />
    </PageTemplate>
  );
}

export default PuzzlePage;