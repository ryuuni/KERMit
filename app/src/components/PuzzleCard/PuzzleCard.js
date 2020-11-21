import './PuzzleCard.css';
import PropTypes from 'prop-types';

export default function PuzzleCard(props) {
  const puzzle = props.puzzle;
  return (
    <div
      className="puzzle-card"
      data-testid="puzzle-card"
      onClick={() => props.onClick(puzzle.puzzleId)}
    >
      <div className="main-info">
        <div className="title">Puzzle {puzzle.puzzleId}</div>
        <div className="status">{puzzle.completed ? "Completed" : "In Progress"}</div>
      </div>
      <div className="details">
        <div className="detail">Difficulty: {puzzle.difficulty}</div>
        <div className="detail">Point Value: {puzzle.pointValue}</div>
      </div>
    </div>
  );
}

PuzzleCard.defaultProps = {
  puzzle: null,
  onClick: null,
};

PuzzleCard.propTypes = {
  puzzle: PropTypes.object,
  onClick: PropTypes.func,
};
