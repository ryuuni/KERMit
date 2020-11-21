import './PuzzleCard.css';
import PropTypes from 'prop-types';

export default function PuzzleCard(props) {
  const puzzle = props.puzzle;
  return (
    <div
      className="puzzle-card"
      data-testid="puzzle-card"
      onClick={() => props.onClick(puzzle.puzzle_id)}
    >
      <div className="main-info">
        <div className="title">Puzzle {puzzle.puzzle_id}</div>
        <div className="status">{puzzle.completed ? "Completed" : "In Progress"}</div>
      </div>
      <div className="details">
        <div className="detail">Difficulty: {puzzle.difficulty}</div>
        <div className="detail">Point Value: {puzzle.point_value}</div>
      </div>
    </div>
  );
}

PuzzleCard.defaultProps = {
  puzzle: null,
  onClick: null,
};

PuzzleCard.propTypes = {
  puzzle: PropTypes.shape({
    puzzle_id: PropTypes.string.isRequired,
    difficulty: PropTypes.number.isRequired,
    completed: PropTypes.bool.isRequired,
    point_value: PropTypes.number.isRequired,
    pieces: PropTypes.arrayOf(PropTypes.shape({
      x_coordinate: PropTypes.number.isRequired,
      y_coordinate: PropTypes.number.isRequired,
      static_piece: PropTypes.bool.isRequired,
      value: PropTypes.number,
    })),
    players: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.number.isRequired,
      first_name: PropTypes.string.isRequired,
      last_name: PropTypes.string.isRequired,
      email: PropTypes.string.isRequired,
    })),
  }),
  onClick: PropTypes.func,
};
