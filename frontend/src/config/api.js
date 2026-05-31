const trimTrailingSlash = (value) => value.replace(/\/+$/, '');

export const API_BASE_URL = trimTrailingSlash(
  process.env.REACT_APP_API_BASE_URL || 'http://localhost:5050'
);

export const UPLOAD_AND_ANALYZE_URL = `${API_BASE_URL}/api/upload-and-analyze`;