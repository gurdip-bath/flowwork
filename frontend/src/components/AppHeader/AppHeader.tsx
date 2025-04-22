import React from 'react';
// Comment out the actual context import for now
// import { useAuth } from "../../context/AuthContext";

const AppHeader: React.FC = () => {
  // Comment out the real auth context
  // const { user, isAuthenticated, logout } = useAuth();
  
  // using these mock values for testing
  const user = {
    id: 1,
    email: "test@example.com",
    role: "admin"
  };
  const isAuthenticated = true;
  const logout = () => console.log("Logout clicked");
  
  return (
    <header className="bg-white shadow-md px-6 py-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo/Brand */}
        <div className="flex items-center">
          <h1 className="text-xl font-bold text-blue-600">FlowWork HR</h1>
        </div>
        
        {/* User info and actions */}
        {isAuthenticated && user ? (
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="font-medium">Welcome, {user.email}</p>
              <p className="text-sm text-gray-600">{user.role}</p>
            </div>
            
            <button 
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md"
              onClick={logout}
            >
              Logout
            </button>
          </div>
        ) : (
          <div>
            <button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md">
              Login
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default AppHeader;