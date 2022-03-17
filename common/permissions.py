from email import message
from xmlrpc.client import Boolean
from rest_framework import permissions
from apps.v1.accounts.models import User

class IsAdminOrStudio(permissions.BasePermission):
    message = "you are not admin or studio"
    def has_permission(self,request,view):
        try:
            perms = request.user.role in[role for role,name in User.ROLES if name in ['Admin','Studio']]
           
            return perms
        except Exception as e:
            self.message = "Some Error Occurced in authorization"
            return False