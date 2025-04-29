import React from 'react';

const AppHeader: React.FC = () => { 

  // Mock user data for now
  const user = {
    email: "test@example.com",
    role: "admin"
  };

   return (
    <header className="bg-white shadow-md px-6 py-4">
      <div className="container mx-auto">
        <h1 className="text-xl font-bold text-blue-600">FlowWork HR</h1>
        
        <div className='text-right'>  
          <p className='font-medium'>Welcome, {user.email}</p>
          <p className = 'text-sm text-gray-600'>{user.role}</p>
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