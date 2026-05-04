import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import VideoPlayer from './VideoPlayer';

vi.mock('../api/client', () => ({
  getVideoStreamUrl: vi.fn((id) => `http://localhost/api/video/${id}/stream`),
}));

describe('VideoPlayer', () => {
  it('returns null when videoId is not provided', () => {
    const { container } = render(<VideoPlayer videoId={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders video element with correct src', () => {
    render(<VideoPlayer videoId="test-123" />);
    const video = document.querySelector('video');
    expect(video).toBeInTheDocument();
    expect(video.src).toContain('test-123');
  });

  it('has controls attribute', () => {
    render(<VideoPlayer videoId="test-123" />);
    const video = document.querySelector('video');
    expect(video.controls).toBe(true);
  });
});
