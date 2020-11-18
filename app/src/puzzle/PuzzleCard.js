import './PuzzleCard.css';

function PuzzleCard(props) {
    return (
        <div className="puzzle-card" data-testid="puzzle-card" onClick={() => props.onClick('/puzzle/' + props.puzzleId)}>
            <div className="main-info">
                <div className="title">
                    Puzzle {props.puzzleId}
                </div>
                <div className="status">
                    {props.completed ? "Completed" : "In Progress"}
                </div>
            </div>
            <div className="details">
                <div className="detail">
                    Difficulty: {props.difficulty}
                </div>
                <div className="detail">
                    Point Value: {props.pointValue}
                </div>
            </div>
        </div>
    );
}

export default PuzzleCard;
  