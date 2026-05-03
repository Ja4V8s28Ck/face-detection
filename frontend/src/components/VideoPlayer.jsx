import { getVideoStreamUrl } from '../api/client';

function VideoPlayer({ videoId }) {
  if (!videoId) return null;

  const streamUrl = getVideoStreamUrl(videoId);

  return (
    <div className="mt-8">
      <h2 className="mb-4 text-xl font-semibold text-center text-gray-200">Processed Video</h2>
      <video
        controls
        className="mx-auto max-h-100 w-80 rounded-lg shadow-lg border-2"
        src={streamUrl}
      />
    </div>
  );
}

export default VideoPlayer;
