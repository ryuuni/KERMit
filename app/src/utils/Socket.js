import io from "socket.io-client";

const ENDPOINT = "ws://127.0.0.1:5000/";
export const socket = io(ENDPOINT, {query: {auth: "TOKEN"}, transports: ['websocket']});
