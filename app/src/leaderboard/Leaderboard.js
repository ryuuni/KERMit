import './Leaderboard.css';
import React, { Component } from 'react';
import { DataGrid } from '@material-ui/data-grid';

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
        const columns = [
            { field: 'id', headerName: 'Rank', width: 70 },
            { field: 'firstName', headerName: 'First name', width: 130 },
            { field: 'lastName', headerName: 'Last name', width: 130 },
            { field: 'score', headerName: 'Score', width: 90},
        ];
        var rows = [];
        topPlayers.forEach((player, index) => {
            var rowEntry = {id: index+1, firstName: player.first_name, lastName: player.last_name, score: player.score};
            rows.push(rowEntry);
        });
        return (
            <div className="leaderboard">
                {topPlayers.length === 0 && isLoaded && (<div>No players have finished a game.</div>)}
                {isLoaded && topPlayers.length !== 0 && (
                    <div className="table">
                        <DataGrid rows={rows} columns={columns} pageSize={10} />
                    </div>
                 )}
            </div>
        );
    }
  }
  
export default Leaderboard;