import './Puzzles.css';
import React, { Component } from 'react';
import { Redirect } from "react-router-dom";
import PuzzleCard from './PuzzleCard';

class Puzzles extends Component {  
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
            puzzles: [],
            redirect: null,
        }
    }

    componentDidMount() {
        const requestOptions = {
            method: 'GET',
            headers: { Authorization: `Bearer ${this.props.accessToken}` },
        };
        fetch('/puzzles', requestOptions).then(res => res.json()).then(data => {
            this.setState({
                isLoaded: true,
                puzzles: data.puzzles
              });
        });
    }

    redirectToPath(path) {
        this.setState({ redirect: path});
    }

    createGame() {
        const requestOptions = {
            method: 'POST',
            headers: { Authorization: `Bearer ${this.props.accessToken}` },
        };
        fetch('/puzzles?difficulty=0.9&size=2', requestOptions).then(res => res.json()).then(data => {
            this.redirectToPath('/puzzle/'+data.puzzle_id);
        });
    }
  
    render() {
        const { isLoaded, puzzles, redirect } = this.state;
        if (this.state.redirect) {
            return <Redirect to={redirect} />
        }
        return (
            <div className="homepage">
                <button className="new-game-btn" onClick={() => this.createGame()}>
                    Start new puzzle
                </button>
                {puzzles.length === 0 && isLoaded
                    && (<div className="empty-message">
                            You do not currently have any puzzles. Start a new one using the button above!
                        </div>)}
                <div className="puzzle-cards" data-testid="puzzle-cards">
                    {puzzles.map(puzzle => (
                        <PuzzleCard 
                        accessToken={this.props.accessToken}
                        puzzleId={puzzle.puzzle_id} 
                        completed={puzzle.completed}
                        difficulty={puzzle.difficulty}
                        pointValue={puzzle.point_value}
                        key={puzzle.puzzle_id}
                        onClick={path => this.setState({redirect: path})}
                        />
                    ))}
                </div>
            </div>
        );
    }
  }
  
  export default Puzzles;
  