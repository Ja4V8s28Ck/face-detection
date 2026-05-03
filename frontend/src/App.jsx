import { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import VideoPlayer from './components/VideoPlayer';

function App() {
  const [videoId, setVideoId] = useState(null);

  function handleUploadSuccess(result) {
    setVideoId(result.video_id);
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="mx-auto max-w-3xl px-6 py-10">
        <h1 className="mb-8 text-center text-3xl font-bold tracking-tight text-white">
          Face Detection
        </h1>
        <VideoUpload onUploadSuccess={handleUploadSuccess} />
        {videoId && <VideoPlayer videoId={videoId} />}
      </div>
    </div>
  );
}

export default App;
