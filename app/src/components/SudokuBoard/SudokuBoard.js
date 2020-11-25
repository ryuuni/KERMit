import React, { useCallback, useContext, useState } from 'react'
import PropTypes from 'prop-types';
import './SudokuBoard.css'
import SudokuCell from '../SudokuCell/SudokuCell';
import AccessTokenContext from '../../context/AccessTokenContext';
import { socket } from "../../utils/Socket.js";

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

export default function SudokuBoard(props) {
  const { accessToken } = useContext(AccessTokenContext);
  const [solved, setSolved] = useState(props.solved);
  const [checked, setChecked] = useState(false);

  const movePiece = useCallback(async ({ puzzleId, x, y, value, onSuccess }) => {
    const requestOptions = {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'x_coordinate': x,
        'y_coordinate': y,
        'value': value ? Number(value) : null,
      }),
    };
    await fetch(`http://localhost:5000/puzzles/${puzzleId}/piece`, requestOptions)
    socket.emit('move', {puzzle_id:puzzleId});
  }, [accessToken]);

  if (!props.gridState) {
    return <h3 style={{"text-align": "center"}}>Loading puzzle...</h3>;
  }

  return (
    <div>
      <div className="gridContainer">
        {
          props.gridState.map(cell =>
            <SudokuCell
              key={Number(cell.value) * 100 + cell.y_coordinate * 10 + cell.x_coordinate}
              x={cell.x_coordinate}
              y={cell.y_coordinate}
              number={cell.value}
              onNumberChanged={number => {
                movePiece({
                  x: cell.x_coordinate,
                  y: cell.y_coordinate,
                  value: number,
                  puzzleId: props.puzzleId,
                });
              }}
              prefilled={cell.static_piece || props.solved}
            />
          )
        }
      </div>
      {props.solved ? 
        <h2 className="puzzleStatusText">You win!</h2> :
        <div>
          <button className="checkSolutionBtn" onClick={() => {
            getSolution({
              accessToken,
              puzzleId: props.puzzleId,
              onSuccess: json => setSolved(json.discrepancy.length === 0),
            })
            setChecked(true)
          }}>
            Check Answer
          </button>
          {checked ? (
            solved ? 
              <h2 className="puzzleStatusText">You win!</h2> : 
              <h2 className="puzzleStatusText">Something's Not Right...</h2>
            ) : null}
        </div>
      }
    </div>
  );
}

SudokuBoard.defaultProps = {
  gridState: null,
  puzzleId: '',
  solved: false,
};

SudokuBoard.propTypes = {
  gridState: PropTypes.array,
  puzzleId: PropTypes.string.isRequired,
  solved: PropTypes.bool.isRequired,
};
