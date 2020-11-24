import io from "socket.io-client";
// import { SOCKET_URL } from "config";
// import openSocket from "socket.io-client";

const ENDPOINT = "ws://localhost:5000/";
// const socket = openSocket('http://localhost:5000', {transports: ['websocket']});
export const socket = io(ENDPOINT, {transports: ['websocket']});
// export const socket = new WebSocket(ENDPOINT);
socket.on('disconnect', () => {
    socket.removeAllListeners();
});