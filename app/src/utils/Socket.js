import io from "socket.io-client";
// import { SOCKET_URL } from "config";
// import openSocket from "socket.io-client";

const ENDPOINT = "ws://127.0.0.1:5000/";
// const socket = openSocket('http://localhost:5000', {transports: ['websocket']});
export const socket = io(ENDPOINT, {transports: ['websocket']});
// export const socket = new WebSocket(ENDPOINT);
