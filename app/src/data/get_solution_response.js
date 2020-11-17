const PUZZLE_ID = 1;
const COMPLEDED = true;
const DIFFICULTY = 0.5;
const POINT_VALUE = 90;
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

const DISCREPANCY = [
  {
    "x_coordinate": 2,
    "y_coordinate": 0
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 0
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 1
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 1
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 1
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 2
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 2
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 2
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 2
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 2
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 3
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 3
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 3
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 3
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 4
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 5
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 5
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 5
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 5
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 6
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 6
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 6
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 6
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 6
  },
  {
    "x_coordinate": 2,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 4,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 5,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 7,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 7
  },
  {
    "x_coordinate": 0,
    "y_coordinate": 8
  },
  {
    "x_coordinate": 1,
    "y_coordinate": 8
  },
  {
    "x_coordinate": 3,
    "y_coordinate": 8
  },
  {
    "x_coordinate": 6,
    "y_coordinate": 8
  },
  {
    "x_coordinate": 8,
    "y_coordinate": 8
  }
];

export const getSolutionResponse = () => new Response(JSON.stringify({
  "puzzle_id": PUZZLE_ID,
  "completed": COMPLEDED,
  "difficulty": DIFFICULTY,
  "point_value": POINT_VALUE,
  "pieces": PIECES,
  "discrepancy": DISCREPANCY,
}));

export const getSolvedSolutionResponse = () => new Response(JSON.stringify({
  "puzzle_id": PUZZLE_ID,
  "completed": COMPLEDED,
  "difficulty": DIFFICULTY,
  "point_value": POINT_VALUE,
  "pieces": PIECES,
  "discrepancy": [],
}));
