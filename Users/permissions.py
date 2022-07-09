from rest_framework.permissions import BasePermission
from .models import *
class IsMEMBERUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Role=="MEMBER")

class IsLIBRARIANUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.Role=="LIBRARIAN")