from fastapi import Depends, HTTPException, status
from typing import List, Dict

from app.dependencies import get_current_user


def RoleChecker(allowed_roles: List[str]):
    """
    Create a dependency that checks if the current user has one of the allowed roles.
    
    Args:
        allowed_roles: List of roles that are permitted to access the endpoint
        
    Returns:
        A dependency function that will raise an exception if the user doesn't have permission
    """
    
    async def check_user_role(current_user: Dict = Depends(get_current_user)) -> Dict:
        """
        Check if the current authenticated user has the required role.
        
        Args:
            current_user: The current authenticated user data
            
        Returns:
            The current_user dict if authorization succeeds
            
        Raises:
            HTTPException: If the user doesn't have the required role
        """
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
        
    return check_user_role


# Common role checker dependencies
check_admin = RoleChecker(["admin"])
check_hr_or_admin = RoleChecker(["hr", "admin"])
check_authenticated = RoleChecker(["user", "hr", "admin"])  # Any authenticated user