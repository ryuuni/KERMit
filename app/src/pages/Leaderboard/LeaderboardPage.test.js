import React from 'react';
import { render, screen } from "@testing-library/react";
import LeaderboardPage from './LeaderboardPage.js';
import { PLAYERS, EMPTY_PLAYERS } from '../data/mock_leaderboard_data.js'

function setupFetchStub(data) {
  return function fetchStub(_url) {
    return Promise.resolve({
      json: () => Promise.resolve({ players: data }),
    })
  }
}

test('renders with empty leaderboard message', async () => {
  jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PLAYERS));
  render(<LeaderboardPage accessToken="mockToken" />);
  const emptyMessage = await screen.findAllByText(/No players have finished a game./);
  expect(emptyMessage).toHaveLength(1);
  global.fetch.mockClear();
});

test('renders with DataGrid table', async () => {
  jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(PLAYERS));
  render(<LeaderboardPage accessToken="mockToken" />);
  const emptyMessage = screen.queryByText('No players have finished a game.')
  expect(emptyMessage).toBeNull()
  const leaderboardTable = await screen.findAllByTestId('datagrid');
  expect(leaderboardTable).toHaveLength(1);
  global.fetch.mockClear();
});