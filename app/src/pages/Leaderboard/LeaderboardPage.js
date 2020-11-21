import './LeaderboardPage.css';
import React, { useContext, useState, useEffect, useMemo } from 'react';
import { DataGrid } from '@material-ui/data-grid';
import AccessTokenContext from '../../context/AccessTokenContext';

const columns = [
  { field: 'id', headerName: 'Rank', width: 70 },
  { field: 'firstName', headerName: 'First name', width: 130 },
  { field: 'lastName', headerName: 'Last name', width: 130 },
  { field: 'score', headerName: 'Score', width: 90 },
];

const LeaderboardPage = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [topPlayers, setTopPlayers] = useState([]);
  const { accessToken } = useContext(AccessTokenContext);

  useEffect(() => {
    const requestOptions = {
      method: 'GET',
      headers: { Authorization: `Bearer ${accessToken}` },
    };
    fetch('/leaderboard', requestOptions).then(res => res.json()).then(data => {
      setIsLoaded(true);
      setTopPlayers(data.players);
    });
  }, [accessToken]);

  const rows = useMemo(() => topPlayers.map((player, index) => ({
    id: index + 1,
    firstName: player.first_name,
    lastName: player.last_name,
    score: player.score,
  })), [topPlayers]);

  return (
    <div className="leaderboard">
      <h3>hello</h3>
      {isLoaded && (
        topPlayers.length === 0 ? <div>No players have finished a game.</div> :
          (
            <div className="table" data-testid="datagrid" style={{ height: 650, width: '23%' }}>
              <DataGrid rows={rows} columns={columns} pageSize={10} />
            </div>
          )
      )}
    </div>
  );
};

export default LeaderboardPage;