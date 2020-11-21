import React from 'react';
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import Puzzle from '../Puzzle.js';
import Puzzles from '../Puzzles.js';
import { FULL_PUZZLES, EMPTY_PUZZLES } from '../../data/mock_puzzles_data.js';
import {
    BrowserRouter as Router,
    Route,
} from "react-router-dom";

function setupFetchStub(mockResponse) {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve(mockResponse),
      })
    }
}

test('renders create game button', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    render(<Puzzles accessToken="mockToken" />);
    const emptyMessage = await screen.findAllByText(/Start new puzzle/);
    expect(emptyMessage).toHaveLength(1);
    global.fetch.mockClear();
});

test('create game button calls endpoint', async() => {
    const mockFn = jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    const {getByText} = render(<Router><Puzzles accessToken="mockToken" /></Router>);
    fireEvent.click(getByText('Start new puzzle'));
    expect(mockFn).toHaveBeenCalledTimes(2);
    global.fetch.mockClear();
});

test('create game button redirects to puzzle page', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    const {getByText} = render(<Router>
                                    <Puzzles accessToken="mockToken" />
                                    <Route path="/puzzle/:puzzleId">
                                        <Puzzle accessToken={'mockToken'} />
                                    </Route>
                                </Router>);
    fireEvent.click(getByText('Start new puzzle'));
    const initText = await screen.findAllByText(/Loading puzzle/);
    expect(initText.length).toBe(1);
    global.fetch.mockClear();
});

test('renders no puzzles message', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    render(<Puzzles accessToken="mockToken" />);
    const emptyMessage = await screen.findAllByText(/You do not currently have any puzzles./);
    expect(emptyMessage).toHaveLength(1);
    global.fetch.mockClear();
});

test('renders puzzle cards for user with >0 puzzles', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    const { queryByTestId } = render(<Puzzles accessToken="mockToken" />);
    const puzzleCardsContainer = queryByTestId('puzzle-cards');
    expect(puzzleCardsContainer).not.toBeNull();
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    global.fetch.mockClear();
});