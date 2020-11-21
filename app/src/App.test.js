import { render, within } from '@testing-library/react';
import App from './App';

test('App renders a <GoogleBtn />', () => {
  const { getByTestId } = render(<App />);
  const app = getByTestId('app')
  const googleBtn = within(app).getAllByTestId('login-btn')
  expect(googleBtn.length).toBe(1);
});
