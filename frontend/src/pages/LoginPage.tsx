import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginForm from '../components/LoginForm/LoginForm';

// Manages the page context and layout

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, error, isLoading } = useAuth();

  const handleLogin = async (email: string, password: string) => {
    try {
      await login (email, password);
      console.log('7. Navigating to dashboard')

      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
    };
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">FlowWork HR</h1>
        <p className="text-gray-600">Sign in to your account</p>
      </div>
      
      {isLoading && <div className="text-center mb-4">Loading...</div>}

      {error && (
        <div className="max-w-md mx-auto mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <LoginForm 
      onSubmit={handleLogin}
      isLoading={isLoading}
      error={error} />
    </div>
  );
};

export default LoginPage;