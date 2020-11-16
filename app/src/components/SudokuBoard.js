import React, { Component } from 'react'
import range from 'lodash.range'
import './SudokuBoard.css'
import SudokuCell from './SudokuCell'

class SudokuBoard extends Component {
  render() {
    const cells = range(9).map(rowNum => 
      <tr>{
      range(9).map(colNum => 
        <SudokuCell
          key={colNum}
          number={0}
          prefilled={false}
        />
        )
      }</tr>
    )

    return (
      <table class="grid-container">
        {cells}
      </table>
    );
  }  
}

export default SudokuBoard;