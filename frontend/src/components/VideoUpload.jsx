import { useState } from 'react';
import { uploadVideo } from '../api/client';

function VideoUpload({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  async function handleUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    setProgress(0);

    try {
      const result = await uploadVideo(file, (p) => setProgress(p));
      onUploadSuccess(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="rounded-xl border-2 border-dashed border-gray-700 bg-gray-800 p-6 text-center">
      <h2 className="mb-4 text-xl font-semibold text-gray-200">Upload Video</h2>
      <input
        type="file"
        accept="video/*"
        onChange={handleUpload}
        disabled={uploading}
        className="mx-auto block cursor-pointer file:mr-4 file:rounded-lg file:border-0 file:bg-gray-700 file:px-4 file:py-2 file:text-sm file:font-medium file:text-gray-200 hover:file:bg-gray-600 disabled:cursor-not-allowed disabled:opacity-50"
      />
      {uploading && (
        <div className="mt-4">
          <p className="mb-2 text-md font-mono text-gray-300">
            {progress >= 100 ? "Mapping ROI..." : "Processing video..."}
          </p>
          <div className="h-2 w-full overflow-hidden rounded-full bg-gray-700">
            <div
              className="h-full bg-blue-600 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}
      {error && <p className="mt-3 text-sm text-red-400">{error}</p>}
    </div>
  );
}

export default VideoUpload;
