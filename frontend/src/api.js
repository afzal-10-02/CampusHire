import axios from 'axios';
import router from '@/router'; 

// Use environment variables for production flexibility
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});


// Request Interceptor: Attach Auth Token
apiClient.interceptors.request.use(
  (config) => {
    // FIX: Changed 'token' to 'access_token' to match your login method
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Handle Global Errors Safely
// apiClient.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     // Check if the error is a 401 (Unauthorized/Expired)
//     const isUnauthorized = error.response && error.response.status === 401;

//     if (isUnauthorized) {
//       console.warn('Session expired or unauthorized. Logging out...');
      
//       // FIX: Clean up all items saved during login
//       localStorage.removeItem('access_token');
//       localStorage.removeItem('role');
      
//       // FIX: Use vue-router to redirect without a full page refresh
//       router.push('/login'); 
//     }
    
//     return Promise.reject(error);
//   }
// );

export default apiClient;
