import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import VideoUpload from './VideoUpload';

vi.mock('../api/client', () => ({
  uploadVideo: vi.fn(),
}));

describe('VideoUpload', () => {
  const mockOnSuccess = vi.fn();

  it('renders upload heading', () => {
    render(<VideoUpload onUploadSuccess={mockOnSuccess} />);
    expect(screen.getByText('Upload Video')).toBeInTheDocument();
  });

  it('does not show progress bar initially', () => {
    render(<VideoUpload onUploadSuccess={mockOnSuccess} />);
    expect(screen.queryByText('Processing video...')).not.toBeInTheDocument();
  });

  it('does not show error initially', () => {
    render(<VideoUpload onUploadSuccess={mockOnSuccess} />);
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });
});
