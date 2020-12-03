import React, { useCallback, useMemo, useContext, useState, forwardRef } from 'react'
import PropTypes from 'prop-types';
import './SudokuBoard.css'
import SudokuCell from '../SudokuCell/SudokuCell';
import CurrentUserContext from '../../context/CurrentUserContext';
import Endpoint from '../../utils/Endpoint';

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

const SudokuBoard = forwardRef((props, socket) => {
  const { accessToken, userEmail } = useContext(CurrentUserContext);
  const [solved, setSolved] = useState(props.solved);
  const [checked, setChecked] = useState(false);
  const {playersLockingCells, players} = props;

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
    await fetch(Endpoint.movePiece({puzzleId}), requestOptions);
    socket.current.emit('move', {puzzle_id:puzzleId});
  }, [accessToken, socket]);
  
  const currentPlayer = useMemo(() => players.find(p => p.email === userEmail), [players, userEmail]);
  const addLock = useCallback(({puzzleId, x, y}) => {
    socket.current.emit('add_lock', {puzzle_id: puzzleId, x_coordinate: x, y_coordinate: y, player: currentPlayer});
  }, [socket, currentPlayer]);

  const removeLock = useCallback(({puzzleId, x: x_coordinate, y: y_coordinate}) => {
    socket.current.emit('remove_lock', {puzzle_id: puzzleId, x_coordinate, y_coordinate});
  }, [socket]);

  if (!props.gridState) {
    return <h3 style={{textAlign: "center"}}>Loading puzzle...</h3>;
  }

  return (
    <div>
      <div className="gridContainer">
        {
          props.gridState.map(({value, x_coordinate: x, y_coordinate: y, static_piece}) =>
            <SudokuCell
              key={Number(value) * 100 + y * 10 + x}
              x={x}
              y={y}
              addLock={() => addLock({puzzleId: props.puzzleId, x, y})}
              removeLock={() => removeLock({puzzleId: props.puzzleId, x, y})}
              number={value}
              playerData={playersLockingCells[coordsToString(x, y)]}
              onNumberChanged={number => {
                movePiece({
                  x,
                  y,
                  value: number,
                  puzzleId: props.puzzleId,
                });
              }}
              prefilled={static_piece || props.solved}
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
});

function coordsToString(x, y) {
  return `${x},${y}`;
}

SudokuBoard.defaultProps = {
  gridState: null,
  puzzleId: '',
  solved: false,
  players: [],
  playersLockingCells: {},
};

SudokuBoard.propTypes = {
  gridState: PropTypes.array,
  puzzleId: PropTypes.string.isRequired,
  solved: PropTypes.bool.isRequired,
  players: PropTypes.shape({
    id: PropTypes.number.isRequired,
    first_name: PropTypes.string.isRequired,
    last_name: PropTypes.string,
    email: PropTypes.string,
  }).isRequired,
  playersLockingCells: PropTypes.objectOf(PropTypes.shape({
    player: PropTypes.shape({
      id: PropTypes.number.isRequired,
      first_name: PropTypes.string.isRequired,
      last_name: PropTypes.string,
      email: PropTypes.string,
    }).isRequired,
    index: PropTypes.number,
  })).isRequired,
};

export default SudokuBoard;
