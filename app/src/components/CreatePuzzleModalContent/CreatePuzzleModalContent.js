import './CreatePuzzleModalContent.css';
import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';

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

const CreatePuzzleModal = (props) => {
    const classes = useStyles();
    const [selectedDifficulty, setSelectedDifficulty] = useState(0);
    const [modalStyle] = useState(getModalStyle);

    return (
        <div style={modalStyle} className={classes.paper}>
          <h2 className="modal-title">Start new puzzle</h2>
          <div className="difficulty-select">
            <p className="label">
              Difficulty Level: 
            </p>
            <Select
                value={selectedDifficulty}
                onChange={(event) => setSelectedDifficulty(event.target.value)}
                className="select-options"
              >
                <MenuItem value={0.2}>Warmup</MenuItem>
                <MenuItem value={0.3}>Beginner</MenuItem>
                <MenuItem value={0.4}>Easy</MenuItem>
                <MenuItem value={0.5}>Intermediate</MenuItem>
                <MenuItem value={0.6}>Advanced</MenuItem>
                <MenuItem value={0.7}>Expert</MenuItem>
                <MenuItem value={0.8}>Master</MenuItem>
              </Select>
            </div>
          <button className="submit-new-game" onClick={() => props.createGame(selectedDifficulty)}>Create</button>
        </div>
    );
};

export default CreatePuzzleModal;