import React from 'react';
import LoginForm from '../components/LoginForm';

// Manages the page context and layout

const LoginPage: React.FC = () => {
  const handleLogin = (email: string, password: string) => {
    console.log('Login attempt with:', email, password);
    // In a real app, you would call your authentication API here
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center">
      <div className="text-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">FlowWork HR</h1>
        <p className="text-gray-600">Sign in to your account</p>
      </div>
      
      <LoginForm onSubmit={handleLogin} />
    </div>
  );
};

export default LoginPage;