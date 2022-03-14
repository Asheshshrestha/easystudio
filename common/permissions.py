from rest_framework import permissions
from apps.v1.accounts.models import User

class IsAdminOrJournalist(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            return str(request.user.role in[role for role,name in User.ROLES if name in ['Admin','Joural']])
        except Exception as e:
            return False