import React, { useCallback, useContext } from 'react'
import PropTypes from 'prop-types';
import './SudokuBoard.css'
import SudokuCell from '../SudokuCell/SudokuCell';
import AccessTokenContext from '../../context/AccessTokenContext';

export default function SudokuBoard(props) {
  const { accessToken } = useContext(AccessTokenContext);
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
    await fetch(`/puzzles/${puzzleId}/piece`, requestOptions)
  }, [accessToken]);

  if (!props.gridState) {
    return <h3>Loading puzzle {props.puzzleId}...</h3>;
  }

  return (
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
