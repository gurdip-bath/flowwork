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