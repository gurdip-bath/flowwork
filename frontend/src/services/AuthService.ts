import axios from 'axios';

// Set the base URL for API requests
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define response types
interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface UserResponse {
  id: number;
  email: string;
  role: string;
  created_at: string;
  is_active: boolean;
}

// Authentication service methods
const authService = {
  // Login user
  login: async (email: string, password: string): Promise<LoginResponse> => {
    try {
      // API expects username and password fields for OAuth2 compatibility
      const response = await axios.post<LoginResponse>('/api/v1/auth/login', {
        username: email, // Using email as username
        password
      });
      
      // Set token in localStorage
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        // Set default auth header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
      }
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  
  // Register new user
  register: async (email: string, password: string, role: string = 'user'): Promise<UserResponse> => {
    try {
      const response = await axios.post<UserResponse>('/api/v1/auth/register', {
        email,
        password,
        role
      });
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },
  
  // Get current user profile
  getCurrentUser: async (): Promise<UserResponse> => {
    try {
      const response = await axios.get<UserResponse>('/api/v1/users/me');
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },
  
  // Logout user
  logout: (): void => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  },
  
  // Check if user is authenticated (token exists)
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  },
  
  // Set up axios interceptor to handle 401 responses
  setupAxiosInterceptors: (logout: () => void): void => {
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
          // Auto logout if 401 response returned from API
          logout();
          // Redirect to login page if needed
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }
};

export default authService;