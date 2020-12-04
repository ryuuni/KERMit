import './HidePuzzleModal.css';
import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';

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

const HidePuzzleModal = (props) => {
    const classes = useStyles();
    const [modalStyle] = useState(getModalStyle);

    return (
        <div style={modalStyle} className={classes.paper}>
          <h2 className="modal-title">Delete puzzle {props.puzzleId}</h2>
          <div className="modal-section">
            <p>Are you sure you want to delete this puzzle?</p>
          </div>
        <button className="btn" onClick={props.hidePuzzle}>Yes</button>
        <button className="btn" onClick={() => props.setHideModalStatus(false)}>No</button>
      </div>
    );
};

export default HidePuzzleModal;