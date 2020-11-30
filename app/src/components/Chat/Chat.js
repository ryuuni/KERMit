import React, { useCallback, useContext, useState, forwardRef } from 'react'
import PropTypes from 'prop-types';
import './Chat.css'
import CurrentUserContext from '../../context/CurrentUserContext';
import TextField from '@material-ui/core/TextField';
// import Endpoint from '../../utils/Endpoint';

const Chat = forwardRef((props, socket) => {
  const { userName, userEmail } = useContext(CurrentUserContext);
  const [currMessage, setCurrMessage] = useState('');

  const addMessage = useCallback(() => {
    if (currMessage !== '') {
        socket.current.emit('message', {puzzle_id: props.puzzleId, userName: userName, userEmail: userEmail, messageString: currMessage});
        setCurrMessage('');
    }
  }, [currMessage, userName, userEmail, props.puzzleId, socket]);

  return (
    <div className="chat-section">
        <div className="chat-view">
            {
                (props.messages).map((messageObj) => (
                  messageObj.messageString
                ))
            }
        </div>
        <div className="chat-input">
            <TextField 
                id="standard-multiline-flexible" 
                label="Type your message here"
                onChange={event => {
                    setCurrMessage(event.target.value);
                }}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        addMessage();
                    }   
                }}
                value={currMessage}
            />
            <button className="send-message" onClick={() => {
                addMessage();
            }}>Send Message</button>
        </div>
    </div>
  );
});

Chat.defaultProps = {
  messages: [],
};

Chat.propTypes = {
  messages: PropTypes.array,
};

export default Chat;
