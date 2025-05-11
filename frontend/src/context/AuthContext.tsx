import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

// Define types for our authentication state
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

// Define type for user data
interface User {
  id: number;
  email: string;
  role: string;
}

// Define the shape of our context
interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

// Create the authentication context with a default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Custom hook to use the auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Define props for the AuthProvider component
interface AuthProviderProps {
  children: ReactNode;
}

// Create the Auth Provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // Initialize the auth state
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Effect to load user data if token exists
  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setAuthState({
          ...authState,
          isLoading: false,
        });
        return;
      }

      try {
        // Set the token in axios default headers
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Fetch user data
        const response = await axios.get('/api/v1/users/me');
        
        setAuthState({
          user: response.data,
          token,
          isAuthenticated: true,
          isLoading: false,
          error: null,
        });
      } catch (error) {
        // If token is invalid, clear it
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        
        setAuthState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
          error: 'Authentication failed. Please log in again.',
        });
      }
    };

    loadUser();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setAuthState({
      ...authState,
      isLoading: true,
      error: null,
    });

    console.log('[Frontend] Starting login for:', email);

    try {
      // Create form data for OAuth2 compatibility
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      console.log('2. Sending request');

      // Send login request as form data
      const response = await axios.post('/api/v1/auth/login', formData);
      console.log('3. Response:', response.data);

      // Get token from response
      const token = response.data.access_token;
      
      // Store token in local storage
      console.log('4. Token stored in local storage:', token);
      localStorage.setItem('token', token);
      
      
      // Set the token in axios default headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // Fetch user data
      console.log('5. Getting user data');
      const userResponse = await axios.get('/api/v1/users/me');
      console.log('5. User data:', userResponse.data);

      console.log('6. Login complete');
      
      // Update auth state
      setAuthState({
        user: userResponse.data,
        token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error: any) {
      setAuthState({
        ...authState,
        isLoading: false,
        error: error.response?.data?.detail || 'Login failed. Please check your credentials.',
      });
      throw error;
    }
  };

  // Logout function
  const logout = () => {
    // Clear token from local storage
    localStorage.removeItem('token');
    
    // Remove the token from axios default headers
    delete axios.defaults.headers.common['Authorization'];
    
    // Reset auth state
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  };

  // Clear error function
  const clearError = () => {
    setAuthState({
      ...authState,
      error: null,
    });
  };

  // Provide the auth context value
  return (
    <AuthContext.Provider
      value={{
        ...authState,
        login,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

