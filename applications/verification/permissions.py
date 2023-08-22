from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsEmployeePermission(BasePermission):

    def has_permission(self, request, view):
        try:
            request.user.is_employee
        except Exception:
            raise PermissionDenied
        return bool(request.user and request.user.is_employee)


class IsBossPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            request.user.is_boss
        except Exception:
            raise PermissionDenied
        return bool(request.user and request.user.is_boss)
