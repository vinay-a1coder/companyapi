from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create a company.
    """

    def has_permission(self, request, view):
        # breakpoint()
        return request.user.is_authenticated and request.user.is_superuser