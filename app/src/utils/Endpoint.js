const BACKEND_ADDRESS = process.env.REACT_APP_BACKEND_ADDRESS ?? 'localhost';
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT ?? '5000';

const backendRoot = `http://${BACKEND_ADDRESS}:${BACKEND_PORT}`;

export const Endpoint = {
  register: () => `${backendRoot}/register`,
  createPuzzle: ({difficulty, size = 3}) => `${backendRoot}/puzzles?difficulty=${difficulty}&size=${size}`,
  getPuzzles: () => `${backendRoot}/puzzles`,
  movePiece: ({puzzleId}) => `${backendRoot}/puzzles/${puzzleId}/piece`,
  getLoaderboard: () => `${backendRoot}/leaderboard`,
};