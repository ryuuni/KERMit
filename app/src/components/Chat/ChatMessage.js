import './ChatMessage.css';
import React, { useContext } from 'react';
import CurrentUserContext from '../../context/CurrentUserContext';

const ChatMessage = (props) => {
    const { userEmail } = useContext(CurrentUserContext);
    const isUserMessage = props.message.userEmail === userEmail;

    return (
        <div className="chat-message" style={{ marginRight: isUserMessage ? '0px' : 'auto', marginLeft: isUserMessage ? 'auto' : '0px'}}>
            <div className="user-name">
                { isUserMessage ? "" : props.message.userName}
            </div>
            <div className="message-container">
                <div className="message-string">
                    { props.message.messageString }
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;