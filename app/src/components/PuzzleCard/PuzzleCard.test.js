import React from 'react';
import { render, screen } from "@testing-library/react";
import PuzzleCard from './PuzzleCard.js';

test('renders correct text according to params', async() => {
    render(<PuzzleCard accessToken="mockToken"
        puzzleId={2} 
        completed={true}
        difficulty={0.5}
        pointValue={80}
    />);
    const title = await screen.findAllByText(/Puzzle 2/);
    expect(title).toHaveLength(1);
    const completedStatus = await screen.findAllByText(/Completed/);
    expect(completedStatus).toHaveLength(1);
    const difficulty = await screen.findAllByText(/Difficulty: 0.5/);
    expect(difficulty).toHaveLength(1);
    const points = await screen.findAllByText(/Point Value: 80/);
    expect(points).toHaveLength(1);
});

test('renders incomplete message', async() => {
    render(<PuzzleCard accessToken="mockToken"
        puzzleId={2} 
        completed={false}
        difficulty={0.5}
        pointValue={80}
    />);
    const completedStatus = await screen.findAllByText(/In Progress/);
    expect(completedStatus).toHaveLength(1);
});