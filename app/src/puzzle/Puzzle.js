import { useParams } from "react-router-dom";
import { useState, useEffect } from "react"
import SudokuBoard from '../components/SudokuBoard'
// import { getPuzzleResponse } from '../data/get_puzzle_response'
// import { getSolutionResponse, getSolvedSolutionResponse } from '../data/get_solution_response'

const ONE_SECOND_IN_MILLIS = 1000;

async function getPuzzle({accessToken, puzzleId, onSuccess}) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`/puzzles/${puzzleId}`, requestOptions)
  // const response = await Promise.resolve(getPuzzleResponse());
  const json = await response.json();
  onSuccess(json);
}

async function getSolution({accessToken, puzzleId, onSuccess}) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
   const response = await fetch(`/puzzles/${puzzleId}/solution`, requestOptions)
  //const response = await Promise.resolve(getSolvedSolutionResponse());
  const json = await response.json();
  onSuccess(json);
}

function Puzzle(props) {
  const { puzzleId } = useParams();
  const [pieces, setPieces] = useState(null);
  const [solved, setSolved] = useState(false);

  useEffect(() => {
    const getSolutionSubscription = setInterval(() => getSolution({
      accessToken: props.accessToken,
      puzzleId: puzzleId,
      onSuccess: json => setSolved(json.discrepancy.length === 0),
    }), ONE_SECOND_IN_MILLIS);
    const getPuzzleSubscription = setInterval(() => getPuzzle({
      accessToken: props.accessToken,
      puzzleId: puzzleId,
      onSuccess: json => setPieces(
        json.pieces.sort((pieceA, pieceB) =>
          (pieceA.y_coordinate * 10 +  pieceA.x_coordinate) - (pieceB.y_coordinate * 10 +  pieceB.x_coordinate)
      )),
    }), ONE_SECOND_IN_MILLIS);

    return () => {
      clearInterval(getSolutionSubscription);
      clearInterval(getPuzzleSubscription);
    };
  }, [props.accessToken, puzzleId]);

  return (
    <div>
      <SudokuBoard
        data-testid='sudoku-board'
        gridState={pieces}
        puzzleId={puzzleId}
        solved={solved}
        accessToken={props.accessToken}
      />
      {solved ? <h3>You win!</h3> : null}
    </div>
  );
}

export default Puzzle;