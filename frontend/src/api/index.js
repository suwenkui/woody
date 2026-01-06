import axios from 'axios';

// In production (served by Nginx), baseURL should be relative (e.g., '/') so requests go to the same origin.
// In development, we might still want localhost:8000, but using Vite proxy is better.
// For now, let's use an empty string or '/' if in production, or check environment.
// Simplest for this hybrid deployment: Use relative path.
// If running locally with `npm run dev`, you might need to configure Vite proxy or keep localhost:8000.
// Let's use import.meta.env to check mode.

const baseURL = import.meta.env.PROD ? '' : 'http://localhost:8000';

const api = axios.create({
  baseURL: baseURL, 
});

// Add a request interceptor to include the token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
