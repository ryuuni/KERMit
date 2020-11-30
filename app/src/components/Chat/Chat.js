import React, { useCallback, useContext, useState, forwardRef } from 'react'
import PropTypes from 'prop-types';
import './Chat.css'
// import CurrentUserContext from '../../context/CurrentUserContext';
// import Endpoint from '../../utils/Endpoint';

const Chat = forwardRef((props, socket) => {
//   const { accessToken } = useContext(CurrentUserContext);

  return (
    <div>
      Chat goes here.
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
