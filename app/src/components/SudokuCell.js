import React, { useState } from 'react'
import PropTypes from 'prop-types';
import './SudokuCell.css'

export default function SudokuCell(props) {
  const [value, setValue] = useState(props.number);
  if (props.prefilled == true) {
    return (
      <input 
        type="text"
        className="fixedCell" 
        value={value}
        readOnly
      />
    );
  }

  return (
    <input 
      type="text"
      pattern="[1-9]"
      className="inputCell" 
      value={(value) ? value : ''}
      onInput={event => {
        const userInput = (event.target.validity.valid) ? 
        event.target.value : value;
        setValue(userInput)
        }}
    />
  );
};

SudokuCell.defaultProps = {
  number: null,
  prefilled: false,
};

SudokuCell.propTypes = {
  number: PropTypes.number,
  prefilled: PropTypes.bool.isRequired,
};

