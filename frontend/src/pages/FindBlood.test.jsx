import { render, screen } from '@testing-library/react';
import FindBlood from './FindBlood';

test('renders FindBlood component without crashing', () => {
  render(<FindBlood />);
  const linkElement = screen.getByText(/Find Blood/i);
  expect(linkElement).toBeInTheDocument();
});
