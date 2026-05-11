import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

// mock child components so we don't pull in their side effects
jest.mock('./components/FileUpload', () => ({ onAnalysisComplete, onError }) => (
  <div>
    <span>FileUpload</span>
    <button onClick={() => onAnalysisComplete({ transactions: [] })}>
      Simulate Upload
    </button>
    <button onClick={() => onError('something went wrong')}>
      Simulate Error
    </button>
  </div>
));

jest.mock('./components/Dashboard', () => ({ onReset }) => (
  <div>
    <span>Dashboard</span>
    <button onClick={onReset}>Reset</button>
  </div>
));

test('renders header and FileUpload by default', () => {
  render(<App />);
  expect(screen.getByText('Personal Finance Analyzer')).toBeInTheDocument();
  expect(screen.getByText('FileUpload')).toBeInTheDocument();
});

test('switches to Dashboard after upload completes', async () => {
  render(<App />);
  await userEvent.click(screen.getByText('Simulate Upload'));
  expect(screen.getByText('Dashboard')).toBeInTheDocument();
});

test('shows error message when upload fails', async () => {
  render(<App />);
  await userEvent.click(screen.getByText('Simulate Error'));
  expect(screen.getByText('something went wrong')).toBeInTheDocument();
});

test('resets back to FileUpload after error', async () => {
  render(<App />);
  await userEvent.click(screen.getByText('Simulate Error'));
  await userEvent.click(screen.getByText('Try Again'));
  expect(screen.getByText('FileUpload')).toBeInTheDocument();
});

test('resets back to FileUpload from Dashboard', async () => {
  render(<App />);
  await userEvent.click(screen.getByText('Simulate Upload'));
  await userEvent.click(screen.getByText('Reset'));
  expect(screen.getByText('FileUpload')).toBeInTheDocument();
});