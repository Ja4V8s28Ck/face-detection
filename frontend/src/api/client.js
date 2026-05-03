const API_BASE = window.location.origin;

export async function uploadVideo(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);

  const xhr = new XMLHttpRequest();

  return new Promise((resolve, reject) => {
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable && onProgress) {
        const percent = Math.round((e.loaded / e.total) * 100);
        onProgress(percent);
      }
    });

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject(new Error(`Upload failed: ${xhr.statusText}`));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Network error during upload'));
    });

    xhr.open('POST', `${API_BASE}/api/video/upload`);
    xhr.send(formData);
  });
}

export function getVideoStreamUrl(videoId) {
  return `${API_BASE}/api/video/${videoId}/stream`;
}

export async function getRoiData(videoId) {
  const response = await fetch(`${API_BASE}/api/roi/${videoId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch ROI data: ${response.statusText}`);
  }

  return response.json();
}
