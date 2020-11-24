import './CreatePuzzleModalContent.css';
import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';

function getModalStyle() {
    const top = 50;
    const left = 50;
  
    return {
      top: `${top}%`,
      left: `${left}%`,
      transform: `translate(-${top}%, -${left}%)`,
    };
  }
  
const useStyles = makeStyles((theme) => ({
    paper: {
        color: 'rgb(43, 43, 43)',
        display: 'flex', 
        flexDirection: 'column',
        position: 'absolute',
        width: 400,
        backgroundColor: theme.palette.background.paper,
        border: '2px solid #000',
        boxShadow: theme.shadows[5],
        padding: theme.spacing(2, 4, 3),
    },
}));

const difficultyValues = {
  'Warmup': 0.2,
  'Beginner': 0.3,
  'Easy': 0.4,
  'Intermediate': 0.5,
  'Advanced': 0.6,
  'Expert': 0.7,
  'Master': 0.8,
};

const CreatePuzzleModal = (props) => {
    const classes = useStyles();
    const [selectedDifficulty, setSelectedDifficulty] = useState(0);
    const [additionalPlayers, setAdditionalPlayers] = useState([]);
    const [modalStyle] = useState(getModalStyle);

    return (
        <div style={modalStyle} className={classes.paper}>
          <h2 className="modal-title">Start new puzzle</h2>
          <div className="modal-section">
            <p className="label">
              Difficulty Level: 
            </p>
            <Select
              value={selectedDifficulty}
              onChange={(event) => setSelectedDifficulty(event.target.value)}
              className="select-options"
            >
              {
                Object.entries(difficultyValues).map(([difficultyLabel, value]) => (
                  <MenuItem value={value}>{difficultyLabel}</MenuItem>
                ))
              }
            </Select>
          </div>
          <div className="modal-section">
            <p className="label">Invite Friends: </p>
            <TextField 
              id="standard-basic" 
              label="user1@sample.com, user2@sample.com" 
              onChange={event => {
                const additionalPlayers = event.target.value.replace(' ', '').split(',').filter(player => player);
                setAdditionalPlayers(additionalPlayers);
              }}
              error={additionalPlayers.length && additionalPlayers.some(player => !/@.*\./.test(player))}
            />
          </div>
        <button className="submit-new-game" onClick={() => props.createGame({difficulty: selectedDifficulty, additionalPlayers})}>Create</button>
      </div>
    );
};

export default CreatePuzzleModal;