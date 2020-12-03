import React, { useCallback, useContext, useEffect, useState, forwardRef } from 'react'
import PropTypes from 'prop-types';
import './Chat.css'
import CurrentUserContext from '../../context/CurrentUserContext';
import TextField from '@material-ui/core/TextField';
import ChatMessage from './ChatMessage';

const Chat = forwardRef((props, socket) => {
  const { userName, userEmail } = useContext(CurrentUserContext);
  const [currMessage, setCurrMessage] = useState('');
  const [chatList, setChatList] = useState(null);

  const scrollToBottom = useCallback(() => {
    const scrollHeight = chatList.scrollHeight;
    const height = chatList.clientHeight;
    const maxScrollTop = scrollHeight - height;
    chatList.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
  }, [chatList]);

  useEffect(() => {  
    if (chatList !== null) {
        scrollToBottom();
    }
  }, [scrollToBottom, chatList, props.messages]);

  const addMessage = useCallback(() => {
    if (currMessage !== '') {
        socket.current.emit('message', {puzzle_id: props.puzzleId, userName: userName, userEmail: userEmail, messageString: currMessage});
        setCurrMessage('');
    }
  }, [currMessage, userName, userEmail, props.puzzleId, socket]);

  return (
    <div className="chatSection">
        <div className="chat-label">Chat</div>
        <div className="chat-view" ref={(div) => {
            setChatList(div);
        }}>
            {
                (props.messages).map((messageObj) => (
                  <ChatMessage message={messageObj} />
                ))
            }
        </div>
        <div className="chat-input">
            <TextField 
                className="text-field"
                id="standard-multiline-flexible" 
                placeholder="Type your message here!" 
                onChange={event => {
                    setCurrMessage(event.target.value);
                }}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        addMessage();
                    }   
                }}
                rows={2}
                value={currMessage}
            />
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
