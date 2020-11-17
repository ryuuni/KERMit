import './Leaderboard.css';
import React, { Component } from 'react';

class Leaderboard extends Component {  
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
            topPlayers: []
        }
    }

    componentDidMount() {
        const requestOptions = {
            method: 'GET',
            headers: { Authorization: `Bearer ${this.props.accessToken}` },
        };
        console.log(this.props.accessToken);
        fetch('/leaderboard', requestOptions).then(res => res.json()).then(data => {
            this.setState({
                isLoaded: true,
                topPlayers: data.players
              });
        });
    }
  
    render() {
        const { isLoaded, topPlayers} = this.state;
        return (
            <div className="leaderboard">
                {isLoaded && (<div>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Ranking</th>
                                <th>First Name</th>
                                <th>Last Name</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {topPlayers.map((player, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{player.first_name}</td>
                                    <td>{player.last_name}</td>
                                    <td>{player.score}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>)}
            </div>
        );
    }
  }
  
  export default Leaderboard;