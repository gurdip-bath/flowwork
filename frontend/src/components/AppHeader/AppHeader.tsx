import { useAuth } from "../../context/AuthContext";

const AppHeader: React.FC = () => {
  // Get auth context data
  const { user, isAuthenticated, logout } = useAuth();
  
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