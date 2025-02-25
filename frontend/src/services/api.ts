import axios from 'axios';
import { ICredentials } from 'contexts/AppContext';

// Create an axios instance with base URL and default headers
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    // Handle token refresh or redirect to login on 401 errors
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Either try to refresh the token or redirect to login
      try {
        // Attempt to refresh token (if you implement this feature)
        // const refreshResponse = await api.post('/auth/refresh');
        // localStorage.setItem('authToken', refreshResponse.data.token);
        // originalRequest.headers['Authorization'] = `Bearer ${refreshResponse.data.token}`;
        // return api(originalRequest);
        
        // For now, just logout
        localStorage.removeItem('authToken');
        window.location.href = '/login';
      } catch (refreshError) {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// API methods organized by resource
export const authApi = {
  login: (credentials: ICredentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  // register: (userData) => api.post('/auth/register', userData),
};

// export const usersApi = {
//   getProfile: () => api.get('/users/me'),
//   updateProfile: (userData) => api.put('/users/me', userData),
// };

// Add more API methods as needed

export default api;