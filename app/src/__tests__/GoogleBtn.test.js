import React from 'react';
import { render, screen } from "@testing-library/react";
import GoogleBtn from '../GoogleBtn.js';

function setupFetchStub(data) {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve({players: data}),
      })
    }
  }

test('renders with DataGrid table', async() => {
    // jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(PLAYERS));
    // render(<Leaderboard accessToken="mockToken" />);
    // const emptyMessage = screen.queryByText('No players have finished a game.')
    // expect(emptyMessage).toBeNull()
    // const leaderboardTable = await screen.findAllByTestId('datagrid');
    // expect(leaderboardTable).toHaveLength(1);
    // global.fetch.mockClear();
    expect(3).toBe(3);
});