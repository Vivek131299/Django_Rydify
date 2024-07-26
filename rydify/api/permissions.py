from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user and (request.user.groups.filter(name='Customers').exists() or request.user.is_superuser)


class IsDriver(BasePermission):

    def has_permission(self, request, view):
        return request.user and (request.user.groups.filter(name='Drivers').exists() or request.user.is_superuser)
