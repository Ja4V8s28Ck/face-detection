import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the title', () => {
    render(<App />);
    expect(screen.getByText('Face Detection')).toBeInTheDocument();
  });

  it('renders the upload section', () => {
    render(<App />);
    expect(screen.getByText('Upload Video')).toBeInTheDocument();
  });

  it('does not show video player before upload', () => {
    render(<App />);
    expect(screen.queryByText('Processed Video')).not.toBeInTheDocument();
  });
});
