from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.groups.filter(name="student").exists()
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.groups.filter(name="manager").exists()
        )


class IsDVMUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.groups.filter(name="dvm").exists()
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or request.user.is_superuser
        )

