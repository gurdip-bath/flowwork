import React, { useState } from 'react';
import * as Yup from 'yup';


interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
}

// Define validation schema
const LoginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required'),
});

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
  isLoading?: boolean;
  error?: string | null;
  };


// Focused only on form functionality
const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, isLoading, error }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

 const handleSubmit = (event: React.FormEvent) => {
  event.preventDefault();
  
  try {
    LoginSchema.validateSync({ email, password });
    onSubmit(email, password);
  
  } catch (error) {
    console.error('Validation error:', error);
  }
};

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={isLoading}  
          className={`w-full font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline
            ${isLoading 
              ? 'bg-blue-300 cursor-not-allowed' 
              : 'bg-blue-500 hover:bg-blue-600'  
            } text-white`}
        > 
            {isLoading ? 'Signing In...' : 'Sign In'}  
        </button>
      </form>
    </div>
  );
};

export default LoginForm;

// note to self. currently the form provides a response of Login failed. Please check your credentials.
// need to double check credentials and ensure that the login is working as expected.