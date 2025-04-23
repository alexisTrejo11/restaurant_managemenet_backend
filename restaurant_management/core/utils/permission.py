from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import UntypedToken

class RoleBasedPermission(BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def has_permission(self, request, view):
        try:
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                raise PermissionDenied("Invalid token format")
            
            token = auth_header.split(' ')[1]
            
            token_obj = UntypedToken(token)
            claims = token_obj.payload
            
            role = claims.get('role')

            if role in self.allowed_roles:
                return True
            
            raise PermissionDenied("You do not have permission to access this resource.")
        except Exception as e:
            print(f"Error: {str(e)}")
            raise PermissionDenied(f"Permission error: {str(e)}")