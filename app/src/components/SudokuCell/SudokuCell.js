import React, { useState } from 'react'
import PropTypes from 'prop-types';
import './SudokuCell.css'

export default function SudokuCell(props) {
  const [value, setValue] = useState(props.number);
  const style = {};
  if (props.x % 3 === 0) {
    style.borderLeft = '3px solid black';
  }
  if (props.y % 3 === 0) {
    style.borderTop = '3px solid black';
  }
  style.borderRight = (props.x % 3 === 2) ? '3px solid black' : 'none';
  style.borderBottom = (props.y % 3 === 2) ? '3px solid black' : 'none';

  const className = props.prefilled ? 'fixedCell' : 'inputCell';
  return (
    <input 
      type="text"
      pattern="[1-9]"
      className={className}
      style={style}
      readOnly={props.prefilled}
      value={value || ''}
      onInput={event => {
        const userInput = (event.target.validity.valid) ? 
          event.target.value : value;

        if (value !== userInput) {        
          setValue(userInput);
          props.onNumberChanged(userInput);
        }
      }}
    />
  );
};

SudokuCell.defaultProps = {
  number: null,
  prefilled: false,
  onNumberChanged: () => {},
  x: 0,
  y: 0,
};

SudokuCell.propTypes = {
  number: PropTypes.number,
  prefilled: PropTypes.bool.isRequired,
  onNumberChanged: PropTypes.func,
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
};

