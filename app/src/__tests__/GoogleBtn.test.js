import React from 'react';
import { render, screen } from "@testing-library/react";
import GoogleBtn from '../GoogleBtn.js';

test('initially renders login button', async() => {
    const { getAllByText } = render(<GoogleBtn />);
    const logInMessage = getAllByText('Login');
    expect(logInMessage.length).toBe(1);
});