import React, { useState } from 'react'
import PropTypes from 'prop-types';
import './SudokuCell.css'

export default function SudokuCell(props) {
  // const {value, prefilled} = props;
  const [value, setValue] = useState('');

  return (
    <td>
      <input 
        type="text"
        pattern="[1-9]"
        className="basicCell" 
        value={value}
        onInput={event => {
          const userInput = (event.target.validity.valid) ? 
          event.target.value : value;
          setValue(userInput)
          }}
      />
    </td>
  );
};

SudokuCell.defaultProps = {
  number: null,
  prefilled: false,
};

SudokuCell.propTypes = {
  number: PropTypes.number.isRequired,
  prefilled: PropTypes.bool.isRequired,
};

