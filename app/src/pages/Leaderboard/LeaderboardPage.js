import './LeaderboardPage.css';
import React, { useContext, useState, useEffect, useMemo } from 'react';
import { DataGrid } from '@material-ui/data-grid';
import { makeStyles } from '@material-ui/core/styles';
import AccessTokenContext from '../../context/AccessTokenContext';
import PageTemplate from '../Template/PageTemplate';

const columns = [
  { field: 'id', headerName: 'Rank', width: 90 },
  { field: 'firstName', headerName: 'First name', width: 150 },
  { field: 'lastName', headerName: 'Last name', width: 150 },
  { field: 'score', headerName: 'Score', width: 90 },
];

const useStyles = makeStyles((theme) => ({
  root: {
    border: 0,
    color: 'rgba(0,0,0,.85)',
    backgroundColor: 'white',
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    WebkitFontSmoothing: 'auto',
    letterSpacing: 'normal',
    '& .MuiDataGrid-columnsContainer': {
      backgroundColor: '#fafafa',
    },
    '& .MuiDataGrid-iconSeparator': {
      display: 'none',
    },
    '& .MuiDataGrid-colCell, .MuiDataGrid-cell': {
      borderRight: `1px solid #f0f0f0`,
    },
    '& .MuiDataGrid-columnsContainer, .MuiDataGrid-cell': {
      borderBottom: `1px solid #f0f0f0`,
    },
    '& .MuiDataGrid-cell': {
      color: 'rgba(0,0,0,.85)',
    },
  },
}));

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
      if (data.players !== undefined) {
        setTopPlayers(data.players);
      }
    });
  }, [accessToken]);

  const rows = useMemo(() => topPlayers.map((player, index) => ({
    id: index + 1,
    firstName: player.first_name,
    lastName: player.last_name,
    score: player.score,
  })), [topPlayers]);

  const tableStyle = useStyles();

  return (
    <PageTemplate>
      <div className="leaderboard">
        {isLoaded && (
          topPlayers.length === 0 ? <div className="empty-message">No players have finished a game.</div> :
            (
              <div className="table" data-testid="datagrid" style={{ height: 650, width: 480 }}>
                <DataGrid className={tableStyle.root} rows={rows} columns={columns} pageSize={10} />
              </div>
            )
        )}
      </div>
    </PageTemplate>
  );
};

export default LeaderboardPage;