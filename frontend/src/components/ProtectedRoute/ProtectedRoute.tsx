import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
}
   const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    // Authentication logic here
    const { isAuthenticated, isLoading } = useAuth();
    const location = useLocation();
    
    // Check if the authentication state is still loading
    if (isLoading) {
        return <div>Loading...</div>
    }   
    // Check if the user is authenticated
    if (isAuthenticated) {
        // If authenticated, return the children components
        return children;
    } else {
        return <Navigate to="/login" state={{ from: location }} replace />;
        // If not authenticated, redirect to the login page
        
    }

}

export default ProtectedRoute;
  // This component is a higher-order component that wraps around the children components and checks if the user is authenticated.
  // If the user is authenticated, it renders the children components. If not, it redirects the user to the login page.
  // This is useful for protecting routes that require authentication, such as the dashboard or profile pages.
  // You can use this component in your main App component or in specific routes to ensure that only authenticated users can access certain parts of your application.
  // You can also customize the redirection logic to redirect to a different page or show an error message if needed.
  // Additionally, you can enhance this component by adding features such as loading states, error handling, or role-based access control to further improve the user experience and security of your application.
