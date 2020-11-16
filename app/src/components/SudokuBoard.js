import React, { Component } from 'react'
import range from 'lodash.range'
import './SudokuBoard.css'
import SudokuCell from './SudokuCell'

const PIECES = [
  {
    "x_coordinate": 0,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 7
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 9
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 0,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 4
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 3
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 1
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 0,
    "static_piece": true,
    "value": 5
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 0,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 1,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 1
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 1,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 7
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 6
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 9
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 1,
    "static_piece": true,
    "value": 4
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 1,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 2,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 2,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 2,
    "static_piece": true,
    "value": 6
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 2,
    "static_piece": true,
    "value": 9
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 2,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 2,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 2,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 2,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 2,
    "static_piece": true,
    "value": 1
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 3,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 3,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 3,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 3,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 3,
    "static_piece": true,
    "value": 4
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 3,
    "static_piece": true,
    "value": 9
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 3,
    "static_piece": true,
    "value": 6
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 3,
    "static_piece": true,
    "value": 2
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 3,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 4,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 4,
    "static_piece": true,
    "value": 4
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 4,
    "static_piece": true,
    "value": 1
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 4,
    "static_piece": true,
    "value": 5
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 5,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 5,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 5,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 5,
    "static_piece": true,
    "value": 6
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 5,
    "static_piece": true,
    "value": 1
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 5,
    "static_piece": true,
    "value": 5
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 5,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 5,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 5,
    "static_piece": true,
    "value": 3
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 6,
    "static_piece": true,
    "value": 5
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 6,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 6,
    "static_piece": true,
    "value": 4
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 6,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 6,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 6,
    "static_piece": true,
    "value": 3
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 6,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 6,
    "static_piece": true,
    "value": 6
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 6,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 7,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 7,
    "static_piece": true,
    "value": 7
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 7,
    "static_piece": true,
    "value": 2
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 7,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 8,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 8,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 8,
    "static_piece": true,
    "value": 9
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 8,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 8,
    "static_piece": true,
    "value": 2
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 8,
    "static_piece": true,
    "value": 7
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 8,
    "static_piece": false,
    "value": null
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 8,
    "static_piece": true,
    "value": 8
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 8,
    "static_piece": false,
    "value": null
  }
];


export default function SudokuBoard(props) {
  // const cells = 
  //   <tr>
  //     <SudokuCell number={9} prefilled={true}/>
  //     <SudokuCell number={0} prefilled={false}/>
  //   </tr>
  // const cells = range(9).map(rowNum => 
  //   <tr>{
  //   range(9).map(colNum => 
  //     <SudokuCell
  //       key={rowNum*10+colNum}
  //       number={0}
  //       prefilled={false}
  //     />
  //     )
  //   }</tr>
  // )

  return (
    <div className="gridContainer">
      {
        PIECES.map(cell =>
          <SudokuCell 
            key={cell.x_coordinate*10 + cell.y_coordinate} 
            number={cell.value}
            prefilled={cell.static_piece}
          />
        )
      }
    </div>
  );
}

