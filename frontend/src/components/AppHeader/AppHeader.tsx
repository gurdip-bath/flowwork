import React from 'react';
import { useAuth } from '../../context/AuthContext';

const AppHeader: React.FC = () => { 

  
  const { user, isAuthenticated, logout } = useAuth();
   

  return (
    <header className="bg-secondary/95 backdrop-blur-md text-white shadow-lg border-b border-white/10 px-6 py-4 fixed top-0 left-0 right-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">F</span>
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent">
            FlowWork HR
          </h1>
      </div>
        
        {isAuthenticated && user ? (
          <div className='text-right'>  
            <p className='font-medium'>Welcome, {user.email}</p>
            <p className='text-sm text-gray-300'>{user.role}</p>
          </div>
        ) : (
          <div className='text-right'>
            <p className='text-sm text-gray-300'>Not logged in</p>
          </div>
        )}
         <div className="mb-1">
            <button onClick={logout}
            className="bg-primary hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors">
              Logout
            </button>
          </div>
      </div>
    </header>
  );
};

export default AppHeader;

// add auth awareness, error handling, TS improvements and accessibility features to this component
// 1. **Auth Awareness**: Ensure that the component checks if the user is authenticated before displaying user information. If not authenticated, redirect to the login page or show a message.
// 2. **Error Handling**: Implement error handling to manage any issues that may arise when fetching user data. This could include displaying an error message or a fallback UI.
// 3. **TypeScript Improvements**: Use TypeScript interfaces or types to define the structure of the user data. This will help with type safety and improve code readability. 