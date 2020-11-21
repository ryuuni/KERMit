import { useParams } from "react-router-dom";
import { useState, useEffect, useContext } from "react"
import SudokuBoard from '../../PuzzlePageComponents/SudokuBoard';
import AccessTokenContext from '../../context/AccessTokenContext';
import PageTemplate from '../Template/PageTemplate';
// import { getPuzzleResponse } from '../data/get_puzzle_response'
// import { getSolutionResponse, getSolvedSolutionResponse } from '../data/get_solution_response'

const ONE_SECOND_IN_MILLIS = 1000;

async function getPuzzle({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`/puzzles/${puzzleId}`, requestOptions)
  // const response = await Promise.resolve(getPuzzleResponse());
  const json = await response.json();
  onSuccess(json);
}

async function getSolution({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`/puzzles/${puzzleId}/solution`, requestOptions)
  //const response = await Promise.resolve(getSolvedSolutionResponse());
  const json = await response.json();
  onSuccess(json);
}

const PuzzlePage = () => {
  const { puzzleId } = useParams();
  const [pieces, setPieces] = useState(null);
  const [solved, setSolved] = useState(false);
  const { accessToken } = useContext(AccessTokenContext);

  useEffect(() => {
    const getSolutionSubscription = setInterval(() => getSolution({
      accessToken,
      puzzleId,
      onSuccess: json => setSolved(json.discrepancy.length === 0),
    }), ONE_SECOND_IN_MILLIS);
    const getPuzzleSubscription = setInterval(() => getPuzzle({
      accessToken,
      puzzleId,
      onSuccess: json => setPieces(
        json.pieces.sort((pieceA, pieceB) =>
          (pieceA.y_coordinate * 10 + pieceA.x_coordinate) - (pieceB.y_coordinate * 10 + pieceB.x_coordinate)
        )),
    }), ONE_SECOND_IN_MILLIS);

    return () => {
      clearInterval(getSolutionSubscription);
      clearInterval(getPuzzleSubscription);
    };
  }, [accessToken, puzzleId]);

  return (
    <PageTemplate>
      {solved ? <h3>You win!</h3> : null}
      <SudokuBoard
        data-testid='sudoku-board'
        gridState={pieces}
        puzzleId={puzzleId}
        solved={solved}
        accessToken={accessToken}
      />
    </PageTemplate>
  );
}

export default PuzzlePage;